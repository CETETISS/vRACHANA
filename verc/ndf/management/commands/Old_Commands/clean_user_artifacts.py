import os
import datetime
import re
try:
    from bson import ObjectId
except ImportError:  # old pymongo
    from pymongo.objectid import ObjectId
from functools import reduce
import operator
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from gnowsys_ndf.ndf.models import node_collection, triple_collection, filehive_collection, counter_collection,benchmark_collection, GSystemType, Author, HistoryManager
from gnowsys_ndf.settings import GSTUDIO_DATA_ROOT, GSTUDIO_LOGS_DIR_PATH, MEDIA_ROOT, GSTUDIO_INSTITUTE_ID, GSTUDIO_INSTITUTE_ID
from export_logic import create_log_file, write_md5_of_dump, get_counter_ids, dump_node
from gnowsys_ndf.ndf.views.methods import delete_node,get_group_name_id

UNIT_IDS = []
UNIT_NAMES = []
log_file = None
log_file_path = None
ann_unit_gst_name, ann_unit_gst_id = GSystemType.get_gst_name_id(u"announced_unit")

def call_exit():
    print "\nExiting..."
    os._exit(0)   

def delete_user_artifacts(user_ids_list):
    print "inside delete_user_artifacts"
    user_ids_list = map(int, user_ids_list)
    print "\n unit_ids ",user_ids_list,UNIT_IDS
    all_nodes = node_collection.find({'_type': 'GSystem', 'created_by': {'$in': user_ids_list}, 'group_set': {'$in': UNIT_IDS}})
    print "\nArtifacts: ", all_nodes.count()
    if all_nodes.count():
      for each_node in all_nodes:
          print ".",
          log_file.write("\n**********************************\n")
          log_file.write("deleting the artifact node {0} created by {1}".format(each_node._id,each_node.created_by))
          delete_node(each_node._id,deletion_type=1)
    else:
      log_file.write("\n**********************************\n")
      log_file.write("No artifacts found for {0}".format(UNIT_IDS))
  
def get_counter_ids(user_ids=None):
    '''
    Fetch all the Counter instances of the exporting Group
    '''
    counter_collection_cur = counter_collection.find({'user_id': {'$in': user_ids},'group_id':{'$in':UNIT_IDS}})
    return counter_collection_cur


def get_bnchmrk_data(visited_nodes,authname):
    '''
    Fetch all the Benchmark instances of the exporting Group
    '''
    print "inside bnchmrkdata",visited_nodes,authname,len(visited_nodes)
    reg = '|'.join(str(elem) for elem in visited_nodes)         
    print "into get_bnchmrk_data",reg
    print "reg str",reg
    regx = re.compile(reg,re.IGNORECASE)
    benchmark_collection_cur = benchmark_collection.find({'user':authname,'calling_url':regx})
    print "bnchmrkdata",benchmark_collection_cur.count() 
    return benchmark_collection_cur

def get_nonadmin_users():
  query = {'member_of': ann_unit_gst_id,'_id':{'$in':UNIT_IDS}}
  print "query:",query
  rec = node_collection.collection.aggregate([
    { "$match": query },
    {  "$group":   {
    '_id': 0,
    'count': { '$sum': 1 } ,
    "author_set": {
      "$addToSet":    "$author_set"
    },
    "group_admin": {
      "$addToSet":    "$group_admin"
    }
    },},

    {  "$project": {
    '_id': 0,
    'total': '$count',
    "user_ids": {
        "$cond":    [
            {
                "$eq":  [
                    "$author_set",
                    []
                ]
            },
            [],
            "$author_set"
        ]
    },
    "admin_ids": {
        "$cond":    [
            {
                "$eq":  [
                    "$group_admin",
                    []
                ]
            },
            [],
            "$group_admin"
        ]
    }

    }
    }
  ])

  for e in rec['result']:
      print e
      user_ids_lists = e['user_ids']
      admin_ids_lists = e['admin_ids']

  user_id_list = reduce(operator.concat, user_ids_lists)
  
  admin_id_list = reduce(operator.concat, admin_ids_lists)
  non_admin_user_id_list = list(set(user_id_list) - set(admin_id_list))
  non_admin_user_id_list = [x for x in non_admin_user_id_list if x is not None]
  return non_admin_user_id_list
  
class Command(BaseCommand):
    def handle(self, *args, **options):
        global UNIT_IDS
        global UNIT_NAMES
        global log_file
        global log_file_path
        
        if args:
          try:
            args_ids = map(ObjectId,args)
          except Exception as e:
            print "\n\nPlease enter Valid ObjectId."
            call_exit()
          all_ann_units_cur = node_collection.find({'_id': {'$in': args_ids}})
          for each_un in all_ann_units_cur:
            UNIT_IDS.append(each_un._id)
            UNIT_NAMES.append(each_un.name)
        else:
          all_ann_units_cur = node_collection.find({'member_of': ann_unit_gst_id})
          print "\nTotal Units : ", all_ann_units_cur.count()
          for ind, each_ann_unit in enumerate(all_ann_units_cur, start=1):
              unit_selection = raw_input("\n\t{0}. Unit: {1} \n\tEnter y/Y to select: ".format(ind, each_ann_unit.name))
              if unit_selection in ['y', 'Y']:
                  print "\t Yes"
                  UNIT_IDS.append(each_ann_unit._id)
                  UNIT_NAMES.append(each_ann_unit.name)
              else:
                  print "\t No"

        print "\nUser Artifacts Cleaning of following Units:"
        print ("\n\t".join(["{0}. {1}".format(i,unit_name) for i, unit_name in enumerate(UNIT_NAMES, 1)]))

        proceed_flag = raw_input("\nEnter y/Y to Confirm: ")
        if proceed_flag:
          try:

            datetimestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file_name = 'artifacts_cleaning_' + str(GSTUDIO_INSTITUTE_ID) + "_"+ str(datetimestamp)

            #TOP_PATH = os.path.join(GSTUDIO_DATA_ROOT, 'data_export',  log_file_name)
            #SCHEMA_MAP_PATH = TOP_PATH

            log_file_path = create_log_file(log_file_name)
            #setup_dump_path()


            log_file = open(log_file_path, 'w+')
            log_file.write("\n######### Script ran on : " + str(datetime.datetime.now()) + " #########\n\n")
            log_file.write("User Artifacts Data Cleaning for Units: " + str(UNIT_IDS))

            print "user_ids", non_admin_user_id_list
            print "unit data cleaning",UNIT_IDS,UNIT_NAMES

            non_admin_user_id_list = get_nonadmin_users()

            if non_admin_user_id_list:
              log_file.write("Users ids: " + str(non_admin_user_id_list))
            
              log_file.write("\n********************************")
              log_file.write("delete_user_artifacts getting triggered")
              delete_user_artifacts(non_admin_user_id_list)
              counternds = get_counter_ids(user_ids=non_admin_user_id_list)
              print "Total counter nodes",counternds.count()
              for eachnd in counternds:
                log_file.write("\n*******************************\n")
                log_file.write("Fetched the counternd of user {0}".format(eachnd.user_id))
                log_file.write("\nFetching the visited nodes of the given group")
                print "counternd",eachnd._id
                #print "visited_nodes",eachnd.visited_nodes.keys()
                visited_actnds = eachnd.visited_nodes.keys()
                authorname = Author.get_author_usernames_list_from_user_id_list([eachnd.user_id])
                #print "before calling bnchmrkdata",visited_actnds,authorid
                if len(visited_actnds) > 0:
                  bnchmrknds = get_bnchmrk_data(visited_actnds,authorname[0])
                  print "bnch",bnchmrknds.count(),type(bnchmrknds)
                  for eachbnchmrknd in bnchmrknds:
                    print "Removing :", eachbnchmrknd['_id']
                    #HistoryManager.delete_json_file(bnchmrk, type(bnchmrk))
                    benchmark_collection.collection.remove({'_id':ObjectId(eachbnchmrknd['_id'])})
                HistoryManager.delete_json_file(eachnd, type(eachnd))
                counter_collection.collection.remove({'_id':ObjectId(eachnd._id)})

              res = node_collection.collection.update({
                  "_type": {'$in': ['GSystem', 'Group']},
                  "contributors": {'$in':non_admin_user_id_list}
              }, {
                  "$pullAll": {"contributors": non_admin_user_id_list}
              },
                  upsert=False, multi=True
              )
              print "\n 7 >> contributors : \n", res

              res1 = node_collection.collection.update({
                  "_type": {'$in': ['GSystem', 'Group']},
                  "author_set": {'$in':non_admin_user_id_list}
              }, {
                  "$pullAll": {"author_set": non_admin_user_id_list}
              },
                  upsert=False, multi=True
              )
              print "\n 7 >> author_set : \n", res1

            else:
              log_file.write("No users with non-admin rights found.")
          except Exception as user_artifacts_cleaning_err:
            log_file.write("Error occurred: " + str(user_artifacts_cleaning_err))
            pass
          finally:
            log_file.write("\n*************************************************************")
            log_file.write("\n######### Script Completed at : " + str(datetime.datetime.now()) + " #########\n\n")
            print "\nSTART : ", str(datetimestamp)
            print "\nEND : ", str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            print "*"*70
            print "\n Log will be found at: ", log_file_path
            print "*"*70
            log_file.close()
            call_exit()
        else:
          call_exit()



# Pending:
# - check for grelation `profile_pic` and other to take decision of which object to keep