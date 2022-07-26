from .base_imports import *
#from .history_manager import HistoryManager
# 
from ndf.gstudio_es.es import *
# from gnowsys_ndf.ndf.views.es_queries import save_to_es
from verc.settings import GSTUDIO_ELASTIC_SEARCH,GSTUDIO_ELASTIC_SEARCH_IN_NODE_CLASS,GSTUDIO_SITE_NAME
#from gnowsys_ndf.ndf.models.models_utils import NodeJSONEncoder,CustomNodeJSONEncoder
# DATABASE Variables
node_collection = db['nodes']

#@connection.register
#print("db:",db['Nodes'])
def _not_empty(val):
    if val.strip() in [None, '']:
        print(val)
        raise ValidationError('name value can not be empty')
def _chk_type_not_empty(val):
    if val in [None, '']:
        raise ValidationError('created_by value can not be empty')

def _chk_access_policy(val):
    if val.strip() in [None, '']:
        raise ValidationError('access_policy value can not be empty')


class Status(EmbeddedDocument):
    score = IntField()
    user_id = IntField()
    ip_address = StringField()


class Node(DynamicDocument):
    #print("db:",db['Nodes'])
    #objects = models.Manager() 
    
    meta = {
        'collection' : 'nodes',
        'allow_inheritance' : True,
        'abstract' : True,
        }
    """
        'indexes' : [
            {
            # 1: Compound index                                                                                                                                        
        'fields' : [
            ('+_type','-name')
        ]
            }, {
                # 2: Compound index                                                                                                                                    
        'fields' : [
            ('+_type','+created_by')
        ]
            },
    ]
    } """
    
    #collection_name = 'Nodes'
    STATUS_CHOICES_TU = (u'DRAFT', u'HIDDEN', u'PUBLISHED', u'DELETED', u'MODERATION')
    #structure = {
    #_type = StringField(Required = True) # check required: required field, Possible
                          # values are to be taken only from the list
                          # NODE_TYPE_CHOICES
    altnames =  StringField(default = u'')
    authors = ListField(IntField(), default = list)
    description =  StringField(default = u'')
    featured = BooleanField()
    content =  StringField(default = u'')
    content_org =  StringField(default = u'')
    name = StringField(Required = True, default = u'',validation=_not_empty)
    submitted_by = IntField(validation=_chk_type_not_empty)
    created_date = ComplexDateTimeField(separator=':',Required = True, default = datetime.datetime.utcnow)
    prior_node =  ListField(ObjectIdField(), default = list)
    post_node =  ListField(ObjectIdField(), default = list)
    last_modified = ComplexDateTimeField(separator=':',default = datetime.datetime.utcnow)
    date_published = ComplexDateTimeField(separator=':',default = datetime.datetime.utcnow)
    modified_by = IntField(), # test required: only ids of Users    
    language = ListField(StringField(), default = ['en','Engilish'])  # Tuple are converted into a simple list
    
    type_of =  ListField(ObjectIdField(), default = list) # check required: only ObjectIDs of GSystemType
    member_of =  ListField(ObjectIdField(), default = list) # check required: only ObjectIDs of
                                 # GSystemType for GSystems, or only
                                 # ObjectIDs of MetaTypes for
                                 # GSystemTypes
    access_policy =  StringField(default = 'public', validation=_chk_access_policy) # check required: only possible
                                  # values are Public or Private.  Why
                                  # is this  StringField()?

    group_set =  ListField(ObjectIdField(), default = list) # check required: should not be
                                 # empty. For type nodes it should be
                                 # set to a Factory Group called
                                 # Administration
    collection_set =  ListField(ObjectIdField(), default = list)  # check required: to exclude
                                       # parent nodes as children, use
                                       # MPTT logic
    tags = ListField(StringField(), default = list)
    
    comment_enabled = BooleanField()
    login_required = BooleanField()
    license =  StringField(default = u'')
    visibility = StringField(choices = STATUS_CHOICES_TU)
    topics = ListField(StringField(), default = list)
    intended_users = StringField(default = u'')
    moderated_by = IntField()
    under_project = StringField(default = u'')
    funded_by = StringField(default = u'')

    
    # Custom functions for the Node class

    def add_in_group_set(self, group_id):
        if group_id not in self.group_set:
            self.group_set.append(ObjectId(group_id))
        return self


    def remove_from_group_set(self, group_id):
        if group_id in self.group_set:
            self.group_set.remove(ObjectId(group_id))
        return self

    def fill_node_values(self, request=HttpRequest(), **kwargs):
        user_id = kwargs.get('submited_by', None)
        # dict to sum both dicts, kwargs and request.POST                                                                                                                                    
        values_dict = {}
        if request:
            if request.POST:
                values_dict.update(request.POST.dict())
            if (not user_id) and request.user:
                user_id = request.user.id
        # adding kwargs dict later to give more priority to values passed via kwargs.                                                                                                        
        values_dict.update(kwargs)

        # handling storing user id values.                                                                                                                                                   
        if user_id:
            if not self['submitted_by'] and ('submitted_by' not in values_dict):
                # if `created_by` field is blank i.e: it's new node and add/fill user_id in it.                                                                                              
                # otherwise escape it (for subsequent update/node-modification).                                                                                                             
                values_dict.update({'submitted_by': user_id})
            if 'modified_by' not in values_dict:
                values_dict.update({'modified_by': user_id})
            if 'contributors' not in values_dict:
                values_dict.update({'authors': add_to_list(self.authors, user_id)})

        if 'member_of' in values_dict  and not isinstance(values_dict['member_of'],ObjectId):
            from gsystem_type import GSystemType
            gst_node = GSystemType.get_gst_name_id(values_dict['member_of'])
            if gst_node:
                values_dict.update({'member_of': ObjectId(gst_node[1])})

        # filter keys from values dict there in node structure.                                                                                                                              
        node_str = Node._fields
        node_str_keys_set = set(node_str.keys())
        values_dict_keys_set = set(values_dict.keys())

        for each_key in values_dict_keys_set.intersection(node_str_keys_set):
            temp_prev_val = self[each_key]
            # checking for proper casting for each field                                                                                                                                     
            if isinstance(node_str[each_key], type):
                node_str_data_type = node_str[each_key].__name__
            else:
                node_str_data_type = node_str[each_key]
            casted_new_val = cast_to_data_type(values_dict[each_key], node_str_data_type)
            # check for uniqueness and addition of prev values for dict, list datatype values                                                                                                
            self[each_key] = casted_new_val
        return self

    @classmethod
    def get_node_by_id(cls, node_id):
        '''                                                                                                                                                                                  
            Takes ObjectId or objectId as string as arg                                                                                                                                      
                and return object                                                                                                                                                            
        '''
        if node_id and (isinstance(node_id, ObjectId) or ObjectId.is_valid(node_id)):
            return node_collection.find_one({'_cls':cls,'_id': ObjectId(node_id)})
        else:
            # raise ValueError('No object found with id: ' + str(node_id))                                                                                                                   
            return None

    @classmethod
    def get_nodes_by_ids_list(cls, node_id_list):
        '''                                                                                                                                                                                  
            Takes list of ObjectIds or objectIds as string as arg                                                                                                                            
                and return list of object                                                                                                                                                    
        '''
        try:
            node_id_list = map(ObjectId, node_id_list)
        except:
            node_id_list = [ObjectId(nid) for nid in node_id_list if nid]

        if node_id_list:
            return node_collection.find({'_cls':cls,'_id': {'$in': node_id_list}})
        else:
            return None
    
    @classmethod
    def get_node_obj_from_id_or_obj(cls, node_obj_or_id, expected_type):
        # confirming arg 'node_obj_or_id' is Object or oid and                                                                                                                               
        # setting node_obj accordingly.                                                                                                                                                      
        node_obj = None

        if isinstance(node_obj_or_id, expected_type):
            node_obj = node_obj_or_id
        elif isinstance(node_obj_or_id, ObjectId) or ObjectId.is_valid(node_obj_or_id):
            node_obj = node_collection.find_one({'_cls':cls,'_id': ObjectId(node_obj_or_id)})
        else:
            # error raised:                                                                                                                                                                  
            raise RuntimeError('No Node class instance found with provided arg for get_node_obj_from_id_or_obj(' + str(node_obj_or_id) + ', expected_type=' + str(expected_type) + ')')

        return node_obj
    
    @classmethod
    def get_name_id_from_type(cls, node_name_or_id, node_type, get_obj=False):
        '''                                                                                                                                                                                  
        e.g:                                                                                                                                                                                 
            Node.get_name_id_from_type('pink-bunny', 'Author')                                                                                                                               
        '''
        if not get_obj:
            # if cached result exists return it                                                                                                                                              

            slug = slugify(node_name_or_id)
            cache_key = node_type + '_name_id' + str(slug)
            cache_result = cache.get(cache_key)

            if cache_result:
                # todo:  return OID after casting                                                                                                                                            
                return (cache_result[0], ObjectId(cache_result[1]))
            # ---------------------------------                                                                                                                                              

        node_id = ObjectId(node_name_or_id) if ObjectId.is_valid(node_name_or_id) else None
        node_obj = node_collection.find_one({
                                        "_cls": {"$in": [
                                                # "GSystemType",                                                                                                                             
                                                # "MetaType",                                                                                                                                
                                                # "RelationType",                                                                                                                            
                                                # "AttributeType",                                                                                                                           
                                                # "Group",                                                                                                                                   
                                                # "Author",                                                                                                                                  
                                                node_type
                                            ]},
                                        "$or":[
                                            {"_id": node_id},
                                            {"name": str(node_name_or_id)}
                                        ]
                                    })

        if node_obj:
            node_name = node_obj.name
            node_id = node_obj._id

            # setting cache with ObjectId                                                                                                                                                    
            cache_key = node_type + '_name_id' + str(slugify(node_id))
            cache.set(cache_key, (node_name, node_id), 60 * 60)

            # setting cache with node_name                                                                                                                                                   
            cache_key = node_type + '_name_id' + str(slugify(node_name))
            cache.set(cache_key, (node_name, node_id), 60 * 60)

            if get_obj:
                return node_obj
            else:
                return node_name, node_id

        if get_obj:
            return None
        else:
            return None, None

    def get_tree_nodes(node_id_or_obj, field_name, level, get_obj=False):
        '''                                                                                                                                                                                  
        node_id_or_obj: root node's _id or obj                                                                                                                                               
        field_name: It can be either of collection_set, prior_node                                                                                                                           
        level: starts from 0                                                                                                                                                                 
        '''
        node_obj = Node.get_node_obj_from_id_or_obj(node_id_or_obj, Node)
        nodes_ids_list = node_obj[field_name]
        while level:
           nodes_ids_cur = Node.get_nodes_by_ids_list(nodes_ids_list)
           nodes_ids_list = []
           if nodes_ids_cur:
               [nodes_ids_list.extend(i[field_name]) for i in nodes_ids_cur]
           level = level - 1

        if get_obj:
            return Node.get_nodes_by_ids_list(nodes_ids_list)

        return nodes_ids_list

    ########## Setter(@x.setter) & Getter(@property) ##########                                                                                                                              
    @property
    def member_of_names_list(self):
        """Returns a list having names of each member (GSystemType, i.e Page,                                                                                                                
        File, etc.), built from 'member_of' field (list of ObjectIds)                                                                                                                        
                                                                                                                                                                                             
        """
        from gsystem_type import GSystemType
        return [GSystemType.get_gst_name_id(gst_id)[0] for gst_id in self.member_of]


    @property
    def group_set_names_list(self):
        """Returns a list having names of each member (Group name),                                                                                                                          
        built from 'group_set' field (list of ObjectIds)                                                                                                                                     
                                                                                                                                                                                             
        """
        from group import Group
        return [Group.get_group_name_id(gr_id)[0] for gr_id in self.group_set]

    @property
    def group_set_names_list(self):
        """Returns a list having names of each member (Group name),                                                                                                                          
        built from 'group_set' field (list of ObjectIds)                                                                                                                                     
                                                                                                                                                                                             
        """
        from group import Group
        return [Group.get_group_name_id(gr_id)[0] for gr_id in self.group_set]


    @property
    def user_details_dict(self):
        """Retrieves names of created-by & modified-by users from the given                                                                                                                  
        node, and appends those to 'user_details' dict-variable                                                                                                                              
                                                                                                                                                                                             
        """
        user_details = {}
        if self.created_by:
            user_details['submitted_by'] = User.objects.get(pk=self.created_by).username

        contributor_names = []
        for each_pk in self.authors:
            #print "user:",User.objects.get(pk=each_pk).username                                                                                                                             
            contributor_names.append(User.objects.get(pk=each_pk).username)
        #print "contributor:",contributor_names                                                                                                                                              
        user_details['authors'] = contributor_names

        if self.modified_by:
            user_details['modified_by'] = User.objects.get(pk=self.modified_by).username

        return user_details

    @property
    def prior_node_dict(self):
        """Returns a dictionary consisting of key-value pair as                                                                                                                              
        ObjectId-Document pair respectively for prior_node objects of                                                                                                                        
        the given node.                                                                                                                                                                      
                                                                                                                                                                                             
        """

        obj_dict = {}
        i = 0
        for each_id in self.prior_node:
            i = i + 1

            if each_id != self._id:
                node_collection_object = node_collection.find_one({"_id": ObjectId(each_id)})
                dict_key = i
                dict_value = node_collection_object

                obj_dict[dict_key] = dict_value

        return obj_dict

    @property
    def collection_dict(self):
        """Returns a dictionary consisting of key-value pair as                                                                                                                              
        ObjectId-Document pair respectively for collection_set objects                                                                                                                       
        of the given node.                                                                                                                                                                   
                                                                                                                                                                                             
        """

        obj_dict = {}
        i = 0;
        for each_id in self.collection_set:
            i = i + 1
            if each_id != self._id:
                node_collection_object = node_collection.find_one({"_id": ObjectId(each_id)})
                dict_key = i
                dict_value = node_collection_object
                obj_dict[dict_key] = dict_value

        return obj_dict

    def __unicode__(self):
        return self._id

    def identity(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        if "is_changed" in kwargs:
            if not kwargs["is_changed"]:
                #print "\n ", self.name, "(", self._id, ") -- Nothing has changed !\n\n"                                                                                                     
                return
        is_new = False
        if not "_id" in self:
            is_new = True               # It's a new document, hence yet no ID!"
            # On save, set "created_at" to current date                                                                                                                                      
            self.created_date = datetime.datetime.today()

        self.last_modified = datetime.datetime.today()

        # Check the fields which are not present in the class       # structure, whether do they exists in their GSystemType's                                                                                                                           
        # "attribute_type_set"; If exists, add them to the document                                                                                                                          
        # Otherwise, throw an error -- " Illegal access: Invalid field                                                                                                                       
        # found!!! "

        try:

            keys_list = self._fields.keys()
            keys_list.append('_id')
            invalid_struct_fields_list = list(set(json.loads(self.to_json()).keys()) - set(keys_list))
            # print '\n invalid_struct_fields_list: ',invalid_struct_fields_list 
            dt = json.loads(self.to_json())                                                                                                            
            if invalid_struct_fields_list:
                for each_invalid_field in invalid_struct_fields_list:
                    if each_invalid_field in dt:
                        dt.pop(each_invalid_field)
                        # print "=== removed ", each_invalid_field, ' : ',                                                                                                                   
            self = eval(self._cls)(**dt)

        except Exception as e:
            print(e)
            pass
        super(Node, self).save(*args, **kwargs) 

    # User-Defined Functions                                                                                                                                                                 
    def get_possible_attributes(self, gsystem_type_id_or_list):
        """Returns user-defined attribute(s) of given node which belongs to                                                                                                                  
        either given single/list of GType(s).                                                                                                                                                
                                                                                                                                                                                             
        Keyword arguments: gsystem_type_id_or_list -- Single/List of                                                                                                                         
        ObjectId(s) of GSystemTypes' to which the given node (self)                                                                                                                          
        belongs                                                                                                                                                                              
                                                                                                                                                                                             
        If node (self) has '_id' -- Node is created; indicating                                                                                                                              
        possible attributes needs to be searched under GAttribute                                                                                                                            
        collection & return value of those attributes (previously                                                                                                                            
        existing) as part of the list along with attribute-data_type                                                                                                                         
                                                                                                                                                                                             
        Else -- Node needs to be created; indicating possible                                                                                                                                
        attributes needs to be searched under AttributeType collection                                                                                                                       
        & return default value 'None' of those attributes as part of                                                                                                                         
        the list along with attribute-data_type                                                                                                                                              
                                                                                                                                                                                             
        Returns: Dictionary that holds follwoing details:- Key -- Name                                                                                                                       
        of the attribute Value, which inturn is a dictionary that                                                                                                                            
        holds key and values as shown below:                                                                                                                                                 
                                                                                                                                                                                             
        { 'attribute-type-name': { 'altnames': Value of AttributeType                                                                                                                        
        node's altnames field, 'data_type': Value of AttributeType                                                                                                                           
        node's data_type field, 'object_value': Value of GAttribute                                                                                                                          
        node's object_value field } }                                                                                                                                                        
                                                                                                                                                                                             
        """

        gsystem_type_list = []
        possible_attributes = {}
        from attribute_type import AttributeType
        # Converts to list, if passed parameter is only single ObjectId                                                                                                                      
        if not isinstance(gsystem_type_id_or_list, list):
            gsystem_type_list = [gsystem_type_id_or_list]
        else:
            gsystem_type_list = gsystem_type_id_or_list

        # Code for finding out attributes associated with each gsystem_type_id in the list                                                                                                   
        for gsystem_type_id in gsystem_type_list:

            # Converts string representaion of ObjectId to it's corresponding ObjectId type, if found                                                                                        
            if not isinstance(gsystem_type_id, ObjectId):
                if ObjectId.is_valid(gsystem_type_id):
                    gsystem_type_id = ObjectId(gsystem_type_id)
                else:
                    error_message = "\n ObjectIdError: Invalid ObjectId (" + str(gsystem_type_id) + ") found while finding attributes !!!\n"
                    raise Exception(error_message)

            # Case [A]: While editing GSystem                                                                                                                                                
            # Checking in Gattribute collection - to collect user-defined attributes' values, if already set!                                                                                
            if "_id" in self:
                # If - node has key '_id'                                                                                                                                                    
                from triple import triple_collection
                attributes = triple_collection.find({'_type': "GAttribute", 'subject': self._id})
                for attr_obj in attributes:
                    # attr_obj is of type - GAttribute [subject (node._id), attribute_type (AttributeType), object_value (value of attribute)]                                               
                    # Must convert attr_obj.attribute_type [dictionary] to node_collection(attr_obj.attribute_type) [document-object]                                                        
                    # PREV: AttributeType.append_attribute(node_collection.collection.AttributeType(attr_obj.attribute_type), possible_attributes, attr_obj.object_value)                    
                    AttributeType.append_attribute(attr_obj.attribute_type, possible_attributes, attr_obj.object_value)

            # Case [B]: While creating GSystem / if new attributes get added                                                                                                                 
            # Again checking in AttributeType collection - because to collect newly added user-defined attributes, if any!                                                                   
            attributes = node_collection.find({'_type': 'AttributeType', 'subject_type': gsystem_type_id})
            for attr_type in attributes:
                # Here attr_type is of type -- AttributeType                                                                                                                                 
                # PREV: AttributeType.append_attribute(attr_type, possible_attributes)                                                                                                       
                AttributeType.append_attribute(attr_type, possible_attributes)

            # type_of check for current GSystemType to which the node belongs to                                                                                                             
            gsystem_type_node = node_collection.find_one({'_id': gsystem_type_id}, {'name': 1, 'type_of': 1})
            if gsystem_type_node.type_of:
                attributes = node_collection.find({'_type': 'AttributeType', 'subject_type': {'$in': gsystem_type_node.type_of}})
                for attr_type in attributes:
                    # Here attr_type is of type -- AttributeType 
                     # Here attr_type is of type -- AttributeType                                                                                                                             
                    AttributeType.append_attribute(attr_type, possible_attributes)

        return possible_attributes


    def get_possible_relations(self, gsystem_type_id_or_list):
        """Returns relation(s) of given node which belongs to either given                                                                                                                   
        single/list of GType(s).                                                                                                                                                             
                                                                                                                                                                                             
        Keyword arguments: gsystem_type_id_or_list -- Single/List of                                                                                                                         
        ObjectId(s) of GTypes' to which the given node (self) belongs                                                                                                                        
                                                                                                                                                                                             
        If node (self) has '_id' -- Node is created; indicating                                                                                                                              
        possible relations need to be searched under GRelation                                                                                                                               
        collection & return value of those relations (previously                                                                                                                             
        existing) as part of the dict along with relation-type details                                                                                                                       
        ('object_type' and 'inverse_name')                                                                                                                                                   
                                                                                                                                                                                             
        Else -- Node needs to be created; indicating possible                                                                                                                                
        relations need to be searched under RelationType collection &                                                                                                                        
        return default value 'None' for those relations as part of the                                                                                                                       
        dict along with relation-type details ('object_type' and        and                                                                                                                             
        'inverse_name')                                                                                                                                                                      
                                                                                                                                                                                             
        Returns: Dictionary that holds details as follows:- Key --                                                                                                                           
        Name of the relation Value -- It's again a dictionary that                                                                                                                           
        holds key and values as shown below:                                                                                                                                                 
                                                                                                                                                                                             
        { // If inverse_relation - False 'relation-type-name': {                                                                                                                             
        'altnames': Value of RelationType node's altnames field [0th                                                                                                                         
        index-element], 'subject_or_object_type': Value of                                                                                                                                   
        RelationType node's object_type field, 'inverse_name': Value                                                                                                                         
        of RelationType node's inverse_name field,                                                                                                                                           
        'subject_or_right_subject_list': List of Value(s) of GRelation                                                                                                                       
        node's right_subject field }                                                                                                                                                         
                                                                                                                                                                                             
          // If inverse_relation - True 'relation-type-name': {                                                                                                                              
          'altnames': Value of RelationType node's altnames field [1st                                                                                                                       
          index-element], 'subject_or_object_type': Value of                                                                                                                                 
          RelationType node's subject_type field, 'inverse_name':                                                                                                                            
          Value of RelationType node's name field,                                                                                                                                           
          'subject_or_right_subject_list': List of Value(s) of                                                                                                                               
          GRelation node's subject field } }                              """
        gsystem_type_list = []
        possible_relations = {}
        from relation_type import RelationType

        # Converts to list, if passed parameter is only single ObjectId                                                                                                                      
        if not isinstance(gsystem_type_id_or_list, list):
            gsystem_type_list = [gsystem_type_id_or_list]
        else:
            gsystem_type_list = gsystem_type_id_or_list

        # Code for finding out relations associated with each gsystem_type_id in the list                                                                                                    
        for gsystem_type_id in gsystem_type_list:

            # Converts string representaion of ObjectId to it's corresponding ObjectId type, if found                                                                                        
            if not isinstance(gsystem_type_id, ObjectId):
                if ObjectId.is_valid(gsystem_type_id):
                    gsystem_type_id = ObjectId(gsystem_type_id)
                else:
                    error_message = "\n ObjectIdError: Invalid ObjectId (" + gsystem_type_id + ") found while finding relations !!!\n"
                    raise Exception(error_message)

            # Relation                                                                                                                                                                       
            inverse_relation = False
            # Case - While editing GSystem Checking in GRelation                                                                                                                             
            # collection - to collect relations' values, if already                                                                                                                          
            # set!                                                                                                                                                                           
            if "_id" in self:
                # If - node has key '_id'                                                                                                                                                    
                from triple import triple_collection
                relations = triple_collection.find({'_type': "GRelation", 'subject': self._id, 'status': u"PUBLISHED"})
                for rel_obj in relations:
                    # rel_obj is of type - GRelation                                                                                                                                         
                    # [subject(node._id), relation_type(RelationType),                                                                                                                       
                    # right_subject(value of related object)] Must                                                                                                                           
                    # convert rel_obj.relation_type [dictionary] to                                                                                                                          
                    # collection.Node(rel_obj.relation_type)                                                                                                                                 
                    # [document-object]                                                                                                                                                      
                    RelationType.append_relation(
                        # PREV:  node_collection.collection.RelationType(rel_obj.relation_type),                                                                                             
                        rel_obj.relation_type,
                        possible_relations, inverse_relation, rel_obj.right_subject
                    )
            # added Checking in RelationType collection - because to                                                                                                                         
            # collect newly added user-defined relations, if any!                                                                                                                            
            relations = node_collection.find({'_type': 'RelationType', 'subject_type': gsystem_type_id})
            for rel_type in relations:
                # Here rel_type is of type -- RelationType                                                                                                                                   
                RelationType.append_relation(rel_type, possible_relations, inverse_relation)

            # type_of check for current GSystemType to which the node                                                                                                                        
            # belongs to                                                                                                                                                                     
            gsystem_type_node = node_collection.find_one({'_id': gsystem_type_id}, {'name': 1, 'type_of': 1})
            if gsystem_type_node.type_of:
                relations = node_collection.find({'_type': 'RelationType', 'subject_type': {'$in': gsystem_type_node.type_of}})
                for rel_type in relations:
                    # Here rel_type is of type -- RelationType                                                                                                                               
                    RelationType.append_relation(rel_type, possible_relations, inverse_relation)

            # Inverse-Relation                                                                                                                                                               
            inverse_relation = True
            # Case - While editing GSystem Checking in GRelation                                                                                                                             
            # collection - to collect inverse-relations' values, if                                                                                                                          
            # already set!                                                                                                                                                                   
            if "_id" in self:
                # If - node has key '_id'                                                                                                                                                    
                from triple import triple_collection
                relations = triple_collection.find({'_type': "GRelation", 'right_subject': self._id, 'status': u"PUBLISHED"})
                for rel_obj in relations:
                    # rel_obj is of type - GRelation                                                                                                                                         
                    # [subject(node._id), relation_type(RelationType),                                                                                                                       
                    # right_subject(value of related object)] Must                                                                                                                           
                    # convert rel_obj.relation_type [dictionary] to                                                                                                                          
                    # collection.Node(rel_obj.relation_type)                                                                                                                                 
                    # [document-object]                                                                                                                                                      
                    rel_type_node = node_collection.one({'_id': ObjectId(rel_obj.relation_type)})
                    if META_TYPE[4] in rel_type_node.member_of_names_list:
                        # We are not handling inverse relation processing for                                                                                                                
                        # Triadic relationship(s)                                                                                                                                            
                        continue

                    RelationType.append_relation(
                        # node_collection.collection.RelationType(rel_obj.relation_type),                                                                                                    
                        rel_obj.relation_type,
                        possible_relations, inverse_relation, rel_obj.subject
                    )
            # Case - While creating GSystem / if new relations get                                                                                                                           
            # added Checking in RelationType collection - because to                                                                                                                         
            # collect newly added user-defined relations, if any!                                                                                                                            
            relations = node_collection.find({'_type': 'RelationType', 'object_type': gsystem_type_id})
            for rel_type in relations:
                # Here rel_type is of type -- RelationType                                                                                                                                   
                RelationType.append_relation(rel_type, possible_relations, inverse_relation)

            # type_of check for current GSystemType to which the node                                                                                                                        
            # belongs to                                                                                                                                                                     
            gsystem_type_node = node_collection.one({'_id': gsystem_type_id}, {'name': 1, 'type_of': 1})
            if gsystem_type_node.type_of:
                relations = node_collection.find({'_type': 'RelationType', 'object_type': {'$in': gsystem_type_node.type_of}})
                for rel_type in relations:
                    # Here rel_type is of type -- RelationType                                                                                                                               
                    RelationType.append_relation(rel_type, possible_relations, inverse_relation)

        return possible_relations


    def get_attribute(self, attribute_type_name, status=None):
        from gattribute import GAttribute
        return GAttribute.get_triples_from_sub_type(self._id, attribute_type_name, status)

    def get_attributes_from_names_list(self, attribute_type_name_list, status=None, get_obj=False):
        from gattribute import GAttribute
        return GAttribute.get_triples_from_sub_type_list(self._id, attribute_type_name_list, status, get_obj)

    def get_relation(self, relation_type_name, status=None):
        from grelation import GRelation
        return GRelation.get_triples_from_sub_type(self._id, relation_type_name, status)


    def get_relation_right_subject_nodes(self, relation_type_name, status=None):
        return node_collection.find({'_id': {'$in': [r.right_subject for r in self.get_relation(relation_type_name)]} })


    def get_neighbourhood(self, member_of):
        """Attaches attributes and relations of the node to itself;                                                                                                                          
        i.e. key's types to it's structure and key's values to itself                                                                                                                        
        """

        attributes = self.get_possible_attributes(member_of)
        for key, value in attributes.iteritems():
                    self.structure[key] = value['data_type']
                    self[key] = value['object_value']

        relations = self.get_possible_relations(member_of)
        for key, value in relations.iteritems():
            self.structure[key] = value['subject_or_object_type']
            self[key] = value['subject_or_right_subject_list']

    @classmethod
    def get_names_list_from_obj_id_list(obj_ids_list, node_type):
        obj_ids_list = map(ObjectId, obj_ids_list)
        nodes_cur = node_collection.find({
                                            '_cls': node_type,
                                            '_id': {'$in': obj_ids_list}
                                        }, {'name': 1})
        result_list = [node['name'] for node in nodes_cur]
        return result_list

    
