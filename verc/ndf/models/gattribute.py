from .base_imports import *
from .triple import *

#@connection.register
class GAttribute(Triple):
    attribute_type_scope = DictField(default = dict),
    attribute_type = ObjectIdField(Required = True),  # ObjectId of AttributeType node                                                                    
       # 'object_value_scope': basestring,                                                                                                                             
    object_value = DynamicField(Required = True)  # value -- it's data-type, is determined by attribute_type field  
    meta = {
       'indexes' : [
               {
               # 1: Compound index                                                                                                                                   
    	        'fields': [
                    ('+_type','+subject','+attribute_type','+status') 
			]
	       }
	    ]
   # check': False  # Required because $id is not explicitly specified in the structure                                                                         
        
        }

