from .base_imports import *
from .node import *
from .gsystem import *

def _val_grp_type(val):
     if val not in TYPES_OF_GROUP:
          raise ValidationError('group_type should be one of the predefined values')
    
def _val_edt_plcy(val):
     if val not in EDIT_POLICY:                                                                                                                               
          raise ValidationError('edit_policy should be one of the predefined values')

def _val_sub_plcy(val):
     if val not in SUBSCRIPTION_POLICY:                                                                                                                               
          raise ValidationError('subscriptn policy should be one of the predefined values')

def _val_vsb_plcy(val):
     if val not in EXISTANCE_POLICY:                                                                                                                               
          raise ValidationError('existance policy should be one of the predefined values')

def _val_disc_plcy(val):
     if val not in LIST_MEMBER_POLICY:                                                                                                                               
          raise ValidationError('disclosure policy should be one of the predefined values')

def _val_encrpt_plcy(val):
     if val not in  ENCRYPTION_POLICY:                                                                                                                               
          raise ValidationError('encrptn policy should be one of the predefined values')

def _val_agncy_plcy(val):
     if val not in GSTUDIO_GROUP_AGENCY_TYPES:                                                                                                                         
          raise ValidationError('agency policy should be one of the predefined values')


#@connection.register
class Group(GSystem):
    """Group class to create collection (group) of members
    """
    group_type=StringField(default = TYPES_OF_GROUP_DEFAULT,validation = _val_grp_type)        # Types of groups - Anonymous, public or private                        
    edit_policy=StringField(default = EDIT_POLICY_DEFAULT,validation = _val_edt_plcy)      # Editing policy of the group - non editable,editable moderated or editablenon-moderated
    #subscription_policy=StringField(default = SUBSCRIPTION_POLICY_DEFAULT,validation = _val_sub_plcy)   # Subscription policy to this group - open, by invitation, by request                                                      
    visibility_policy=StringField(default = EXISTANCE_POLICY_DEFAULT,validation = _val_vsb_plcy)    # Existance of the group - announced or not announced             
    #disclosure_policy=StringField(default = LIST_MEMBER_POLICY_DEFAULT,validation = _val_disc_plcy)     # Members of this group - disclosed or not                    
    #encryption_policy=StringField(default = ENCRYPTION_POLICY_DEFAULT,validation = _val_encrpt_plcy)     # Encryption - yes or no                                      
    agency_type=StringField(default = GSTUDIO_GROUP_AGENCY_TYPES_DEFAULT,validation = _val_agncy_plcy)      # A choice field such as Pratner,Govt.Agency, NGO etc.    
    group_admin=ListField(StringField(), default = list)                # ObjectId of Author class                                                                    
    moderation_level=IntField(default = -1)            # range from 0 till any integer level                                                                           
    project_config=DictField()
    meta = {
        'collection' : 'nodes',
        }
    @staticmethod
    def get_group_name_id(group_name_or_id, get_obj=False):
        '''
          - This method takes possible group name/id as an argument and returns (group-name and id) or group object.

          - If no second argument is passed, as method name suggests, returned result is "group_name" first and "group_id" second.

          - When we need the entire group object, just pass second argument as (boolian) True. In the case group object will be returned.

          Example 1: res_group_name, res_group_id = Group.get_group_name_id(group_name_or_id)
          - "res_group_name" will contain name of the group.
          - "res_group_id" will contain _id/ObjectId of the group.

          Example 2: res_group_obj = Group.get_group_name_id(group_name_or_id, get_obj=True)
          - "res_group_obj" will contain entire object.

          Optimization Tip: before calling this method, try to cast group_id to ObjectId as follows (or copy paste following snippet at start of function or wherever there is a need):
          try:
              group_id = ObjectId(group_id)
          except:
              group_name, group_id = Group.get_group_name_id(group_id)

        '''
        # if cached result exists return it
        if not get_obj:

            slug = slugify(group_name_or_id)
            # for unicode strings like hindi-text slugify doesn't works
            cache_key = 'get_group_name_id_' + str(slug) if slug else str(abs(hash(group_name_or_id)))
            cache_result = cache.get(cache_key)

            if cache_result:
                return (cache_result[0], ObjectId(cache_result[1]))
        # ---------------------------------

        # case-1: argument - "group_name_or_id" is ObjectId
        if ObjectId.is_valid(group_name_or_id):

            group_obj = Group.objects.filter(_id =  ObjectId(group_name_or_id))[0]

            # checking if group_obj is valid
            if group_obj:
                # if (group_name_or_id == group_obj._id):
                group_id = ObjectId(group_name_or_id)
                group_name = group_obj.name

                if get_obj:
                    return group_obj
                else:
                    # setting cache with both ObjectId and group_name
                    cache.set(cache_key, (group_name, group_id), 60 * 60)
                    cache_key = u'get_group_name_id_' + slugify(group_name)
                    cache.set(cache_key, (group_name, group_id), 60 * 60)
                    return group_name, group_id

        # case-2: argument - "group_name_or_id" is group name
        else:
            group_obj =  Group.objects.filter(name = ObjectId(group_name_or_id))[0]
            # checking if group_obj is valid
            if group_obj:
                # if (group_name_or_id == group_obj.name):
                group_name = group_name_or_id
                group_id = group_obj._id

                if get_obj:
                    return group_obj
                else:
                    # setting cache with both ObjectId and group_name
                    cache.set(cache_key, (group_name, group_id), 60*60)
                    cache_key = u'get_group_name_id_' + slugify(group_name)
                    cache.set(cache_key, (group_name, group_id), 60*60)
                    return group_name, group_id

        if get_obj:
            return None
        else:
            return None, None


    def is_gstaff(self, user):
        """
        Checks whether given user belongs to GStaff.
        GStaff includes only the following users of a group:
          1) Super-user (Django's superuser)
          2) Creator of the group (created_by field)
          3) Admin-user of the group (group_admin field)
        Other memebrs (author_set field) doesn't belongs to GStaff.

        Arguments:
        self -- Node of the currently selected group
        user -- User object taken from request object

        Returns:
        True -- If user is one of them, from the above specified list of categories.
        False -- If above criteria is not met (doesn't belongs to any of the category, mentioned above)!
        """

        if (user.is_superuser) or (user.id == self.created_by) or (user.id in self.group_admin):
            print ("superuser:")
            return True
        else:
            auth_obj = node_collection.find_one({'_cls': 'Author', 'created_by': user.id})
            if auth_obj and auth_obj['agency_type'] == 'Teacher':
                print ("with auth_obj")
                return True
        return False


    @staticmethod
    def can_access(user_id, group):
        '''Returns True if user can access (read/edit/write) group resource.
        ARGS:
            - user_id (int): Django User id
            - group (Group or ObjectID or str-of-group-name): It can be either group's
                                                        object or _id or name.
        '''
        if isinstance(group, Group):
            group_obj = group
        else:
            group_obj = Group.get_group_name_id(group, get_obj=True)

        user_query = User.objects.filter(id=user_id)

        if group_obj and user_query:
            return group_obj.is_gstaff(user_query[0]) or (user_id in group_obj.author_set)
        else:
            return False


    @staticmethod
    def can_read(user_id, group):
        if isinstance(group, Group):
            group_obj = group
        else:
            group_obj = Group.get_group_name_id(group, get_obj=True)

        if group_obj:
            if group_obj.group_type == 'PUBLIC':
                return True
            else:
                user_query = User.objects.filter(id=user_id)
                if user_query:
                    return group_obj.is_gstaff(user_query[0]) or (user_id in group_obj.author_set)

        return False


    def fill_group_values(self,
                        request=None,
                        group_type=None,
                        edit_policy=None,
                        subscription_policy=None,
                        visibility_policy=None,
                        disclosure_policy=None,
                        encryption_policy=None,
                        agency_type=None,
                        group_admin=None,
                        moderation_level=None,
                        **kwargs):
        '''
        function to fill the group object with values supplied.
        - group information may be sent either from "request" or from "kwargs".
        - returning basic fields filled group object
        '''
        # gdv: Group default Values
        gdv = Group.default_values.keys()
        # gsdv: GSystem default Values
        gsdv = GSystem.default_values
        [gsdv.pop(each_gsdv, None) for each_gsdv in gdv]

        arguments = locals()
        for field_key, default_val in gsdv.items():
            try:
                if arguments[field_key]:
                    self[field_key] = arguments[field_key]
            except:
                if self.request:
                    self[field_key] = self.request.POST.get(field_key, default_val)
            finally:
                self[field_key] = default_val

        if group_type:
            self.group_type = group_type
        self.fill_gstystem_values(request=request, **kwargs)

        # explicit: group's should not have draft stage. So publish them:
        self.status = u"PUBLISHED"

        return self
    # --- END --- fill_group_values() ------


    # def create(request=None,
    #             group_type=Group.default_values['group_type'],
    #             edit_policy=Group.default_values['edit_policy'],
    #             subscription_policy=Group.default_values['subscription_policy'],
    #             visibility_policy=Group.default_values['visibility_policy'],
    #             disclosure_policy=Group.default_values['disclosure_policy'],
    #             encryption_policy=Group.default_values['encryption_policy'],
    #             agency_type=Group.default_values['agency_type'],
    #             group_admin=Group.default_values['group_admin'],
    #             moderation_level=Group.default_values['moderation_level'],
    #             **kwargs):

    #     new_group_obj = node_collection.collection.Group()

    #     GSystem.fill_gstystem_values(request=None,
    #                         author_set=[],
    #                         **kwargs)


    @staticmethod
    def purge_group(group_name_or_id, proceed=True):

        # fetch group object
        group_obj = Group.get_group_name_id(group_name_or_id, get_obj=True)

        if not group_obj:
            raise Exception('Expects either group "name" or "_id". Got invalid argument or that group does not exists.')

        group_id = group_obj._id

        # get all the objects belonging to this group
        all_nodes_under_gr = node_collection.find({'group_set': {'$in': [group_id]}})

        # separate nodes belongs to one and more groups
        only_group_nodes_cnt = all_nodes_under_gr.clone().where("this.group_set.length == 1").count()
        multi_group_nodes_cnt = all_nodes_under_gr.clone().where("this.group_set.length > 1").count()

        print ("Group:", group_obj.name, "(", group_obj.altnames, ") contains:\n",\
            "\t- unique (belongs to this group only) : ", only_group_nodes_cnt, \
            "\n\t- shared (belongs to other groups too): ", multi_group_nodes_cnt, \
            "\n\t============================================", \
            "\n\t- total: ", all_nodes_under_gr.count())

        if not proceed:
            print ("\nDo you want to purge group and all unique nodes(belongs to this group only) under it?")
            print ('Enter Y/y to proceed else N/n to reject group deletion:')
            to_proceed = raw_input()
            proceed = True if (to_proceed in ['y', 'Y']) else False

        if proceed:
            print ("\nProceeding further for purging of group and unique resources/nodes under it...")
            from gnowsys_ndf.ndf.views.methods import delete_node

            grp_res = node_collection.find({ '$and': [ {'group_set':{'$size':1}}, {'group_set': {'$all': [ObjectId(group_id)]}} ] })
            print ("\n Total (unique) resources to be purge: ", grp_res.count())

            for each in grp_res:
                del_status, del_status_msg = delete_node(node_id=each._id, deletion_type=1 )
                # print del_status, del_status_msg
                if not del_status:
                    print ("*"*80)
                    print ("\n Error node: _id: ", each._id, " , name: ", each.name, " type: ", each.member_of_names_list)
                    print ("*"*80)

            print ("\n Purging group: ")
            del_status, del_status_msg = delete_node(node_id=group_id, deletion_type=1)
            print (del_status, del_status_msg)

            # poping group_id from each of shared nodes under group
            all_nodes_under_gr.rewind()
            print ("\n Total (shared) resources to be free from this group: ", all_nodes_under_gr.count())
            for each_shared_node in all_nodes_under_gr:
                if group_id in each_shared_node.group_set:
                    each_shared_node.group_set.remove(group_id)
                    each_shared_node.save()

            return True

        print ("\nAborting group deletion.")
        return True
