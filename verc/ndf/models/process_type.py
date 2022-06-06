from .base_imports import *
from .attribute_type import *
from .relation_type import *


class ProcessType(Node):
    """A kind of nodetype for defining processes or events or temporal
    objects involving change.
    """
    changing_attributetype_set = ListField(DictField(),default=list)  # List of Attribute Types
    changing_relationtype_set = ListField(DictField(),default=list)    # List of Relation Types
    meta = {
	'collection' : 'nodes',
        }



