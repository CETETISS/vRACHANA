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
from export_logic import create_log_file, write_md5_of_dump, get_counter_ids, dump_node, delete_user_artifacts, get_counter_data, get_bnchmrk_data, get_nonadmin_users
from gnowsys_ndf.ndf.views.methods import delete_node,get_group_name_id

UNIT_IDS = []
UNIT_NAMES = []
log_file = None
log_file_path = None
USER_SERIES = []

ann_unit_gst_name, ann_unit_gst_id = GSystemType.get_gst_name_id(u"announced_unit")


def call_exit():
    print "\nExiting..."
    os._exit(0)   
  
class Command(BaseCommand):
    def handle(self, *args, **options):
        global UNIT_IDS
        global UNIT_NAMES
        global log_file
        global log_file_path
        global USER_SERIES 
        USER_SERIES = ['sp','cc','mz','ct','tg','rj']
        if not args[:2] in USER_SERIES: 
          print "\n\nPlease enter Valid User Series."
          call_exit()
        
        pattern = '-'+args[0]
        rg = re.compile(pattern,re.IGNORECASE)
        #Fetch all the author objects belonging to the given series
        authornds = node_collection.find({'_type':'Author','name':rg})
        
        if authornds.count() > 0:
          all_ann_units_cur = node_collection.find({'member_of': ann_unit_gst_id})
          print "\nTotal Units : ", all_ann_units_cur.count()
          for ind, each_ann_unit in enumerate(all_ann_units_cur, start=1):
            UNIT_IDS.append(each_ann_unit._id)
            UNIT_NAMES.append(each_ann_unit.name)
        
          print "\nUser Artifacts Cleaning of following Units:"
          print ("\n\t".join(["{0}. {1}".format(i,unit_name) for i, unit_name in enumerate(UNIT_NAMES, 1)]))

          proceed_flag = raw_input("\nEnter y/Y to Confirm: ")
          if proceed_flag:
            try:

              datetimestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
              log_file_name = 'users_cleaning_' + str(GSTUDIO_INSTITUTE_ID) + "_"+ str(datetimestamp)

              #TOP_PATH = os.path.join(GSTUDIO_DATA_ROOT, 'data_export',  log_file_name)
              #SCHEMA_MAP_PATH = TOP_PATH

              log_file_path = create_log_file(log_file_name)
              #setup_dump_path()


              log_file = open(log_file_path, 'w+')
              log_file.write("\n######### Script ran on : " + str(datetime.datetime.now()) + " #########\n\n")
              log_file.write("User Cleaning of given series: " + str(UNIT_IDS))

              non_admin_user_id_list = get_nonadmin_users(UNIT_IDS)
              
              final_authset = 

              print "user_ids", non_admin_user_id_list
              print "unit data cleaning",UNIT_IDS,UNIT_NAMES
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