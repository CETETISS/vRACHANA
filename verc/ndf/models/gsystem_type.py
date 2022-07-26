from .base_imports import *
from .node import *
from .meta_type import *
from .process_type import *
from .attribute_type import *
from .meta_type import *

# user should have a list of groups attributeType added should
# automatically be added to the attribute_type_set of GSystemType
#@connection.register
class GSystemType(Node):
    """Class to generalize GSystems
    """
    meta_type_set=ListField(DictField(),default=list)        # List of Metatypes                                                                                 
    attribute_type_set=ListField(DictField(),default=list)  # Embed list of Attribute Type Class as Documents 
    relation_type_set=ListField(DictField(),default=list)    # Holds list of Relation Types
    process_type_set=ListField(DictField(),default=list)     # List of Process Types                                                                                 
    property_order=ListField(default=list)                    # List of user-defined attributes in template-view order    
    
    meta = {
	'collection' : 'nodes',
        }

    @staticmethod
    def get_gst_name_id(gst_name_or_id):
        # if cached result exists return it
        slug = slugify(gst_name_or_id)
        cache_key = 'gst_name_id' + str(slug)
        cache_result = cache.get(cache_key)

        if cache_result:
            return (cache_result[0], ObjectId(cache_result[1]))
        # ---------------------------------

        gst_id = ObjectId(gst_name_or_id) if ObjectId.is_valid(gst_name_or_id) else None
        gst_obj = node_collection.one({
                                        "_type": {"$in": ["GSystemType", "MetaType"]},
                                        "$or":[
                                            {"_id": gst_id},
                                            {"name": unicode(gst_name_or_id)}
                                        ]
                                    })

        if gst_obj:
            gst_name = gst_obj.name
            gst_id = gst_obj._id

            # setting cache with ObjectId
            cache_key = u'gst_name_id' + str(slugify(gst_id))
            cache.set(cache_key, (gst_name, gst_id), 60 * 60)

            # setting cache with gst_name
            cache_key = u'gst_name_id' + str(slugify(gst_name))
            cache.set(cache_key, (gst_name, gst_id), 60 * 60)

            return gst_name, gst_id

        return None, None
