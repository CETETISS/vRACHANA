import os
import datetime
import re
try:
    from bson import ObjectId
except ImportError:  # old pymongo
    from pymongo.objectid import ObjectId
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from gnowsys_ndf.ndf.models import node_collection GSystemType
from gnowsys_ndf.settings import GSTUDIO_DATA_ROOT, GSTUDIO_LOGS_DIR_PATH, MEDIA_ROOT, GSTUDIO_INSTITUTE_ID, GSTUDIO_INSTITUTE_ID
from export_logic import create_log_file

UNIT_IDS = []
UNIT_NAMES = []
log_file = None
log_file_path = None

def call_exit():
    print "\nExiting..."
    os._exit(0)   
  
class Command(BaseCommand):
    def handle(self, *args, **options):
        global UNIT_IDS
        global UNIT_NAMES
        global log_file
        global log_file_path
        try:
            args_ids = map(ObjectId,args)
          except Exception as e:
            print "\n\nPlease enter Valid ObjectId."
            call_exit()
        ann_unit_gst_name, ann_unit_gst_id = GSystemType.get_gst_name_id(u"announced_unit")
        all_ann_units_cur = node_collection.find({'member_of':{'$in':ann_unit_gst_id},'_id': {'$in': args_ids}})
        for each_un in all_ann_units_cur:
          UNIT_IDS.append(each_un._id)
          UNIT_NAMES.append(each_un.name)
          
        print "\nAssests copying from {0} to {1} started",format(UNIT_NAMES[0],UNIT_NAMES[1])
        #print ("\n\t".join(["{0}. {1}".format(i,unit_name) for i, unit_name in enumerate(UNIT_NAMES, 1)]))

        proceed_flag = raw_input("\nEnter y/Y to Confirm: ")
        if proceed_flag:
          try:

            datetimestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file_name = 'assests_copying' + str(GSTUDIO_INSTITUTE_ID) + "_"+ str(datetimestamp)

            #TOP_PATH = os.path.join(GSTUDIO_DATA_ROOT, 'data_export',  log_file_name)
            #SCHEMA_MAP_PATH = TOP_PATH

            log_file_path = create_log_file(log_file_name)
            #setup_dump_path()


            log_file = open(log_file_path, 'w+')
            log_file.write("\n######### Script ran on : " + str(datetime.datetime.now()) + " #########\n\n")
            
            asset_gst_name, asset_gst_id = GSystemType.get_gst_name_id(u"Asset")
            assetnds = node_collection.find({'member_of': asset_gst_id,'group_set':{'$in':[UNIT_IDS[0]]}})
            if assetnds.count() > 0:
              print "\nTotal assets found in {0} are {1}",format(UNIT_NAMES[0],assetnds.count())
              for eachnd in assetnds:
                if not (UNIT_IDS[1] in eachnd.group_set):
                  res1 = node_collection.collection.update({
                    "_type": {'$in': ['GSystem']},
                    "_id": eachnd._id,
                    }, {
                        "$push": {"group_set": UNIT_IDS[1]}
                    },
                        upsert=False, multi=True
                    )
            else:
              log_file.write("No assets found in unit -."+UNIT_NAMES[0])
          except Exception as asset_copying_err:
            log_file.write("Error occurred: " + str(asset_copying_err))
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



