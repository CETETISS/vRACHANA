from .base_imports import *
from .attribute_type import *
from .relation_type import *

#@connection.register
class MetaType(Node):
    """MetaType class: Its members are any of GSystemType, AttributeType,
    RelationType, ProcessType.

    It is used to express the NodeTypes that are part of an
    Application developed using GNOWSYS-Studio. E.g, a GSystemType
    'Page' or 'File' become applications by expressing them as members
    of a MetaType, 'GAPP'.

    """
                                                                                                                                                         
    description=StringField()    # Description (name)                                                                                                              
    attribute_type_set=ListField(DictField(),default=list)  # Embed list of Attribute Type Class as Documents             
    relation_type_set=ListField(DictField(),default=list)    # Holds list of Relation Types
    parent=ObjectIdField()                      # Foreign key to self  
    
    use_dot_notation = True

    meta = {
	'collection' : 'nodes',
        }

    def update_document(document, data_dict):

        def field_value(field, value):

            if field.__class__ in (fields.ListField, fields.SortedListField):
                return [
                    field_value(field.field, item)
                    for item in value
                ]
            if field.__class__ in (
                fields.EmbeddedDocumentField,
                fields.GenericEmbeddedDocumentField,
                fields.ReferenceField,
                fields.GenericReferenceField
            ):
                return field.document_type(**value)
            else:
                return value

        [setattr(
            document, key,
            field_value(document._fields[key], value)
        ) for key, value in data_dict.items()]

        return document

