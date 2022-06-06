from .base_imports import *
from .triple import *

#@connection.register
class GRelation(Triple):
   relation_type_scope=DictField(default = dict),
   # 'relation_type=RelationType,  # DBRef of RelationType Class                                                                                                 
   relation_type=ObjectIdField(),  # ObjectId of RelationType node                                                                                                     
   # 'right_subject_scope=basestring,                                                                                                                            
   # ObjectId's of GSystems Class / List of list of ObjectId's of GSystem Class                                                                                    
   right_subject=ListField(ObjectIdField(),default=list)
   meta = {
	'indexes' : [
			{
 	# 1: Compound index                                                                                                                                            
  		'fields':[
            		('+_type','+subject','+relation_type','+status','+right_subject')
       			 ],
#check=False  # Required because $id is not explicitly specified in the structure                                                                             
 		        }, 
			{
        # 2: Compound index                                                                                                                                            
		'fields': [
            		('+_type','+right_subject','+relation_type','+status')
                         ],
#check=False  # Required because $id is not explicitly specified in the structure                                                                             
                        }
		]			
	}
