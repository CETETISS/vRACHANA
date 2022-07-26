''' -- imports from python libraries -- '''
# import os -- Keep such imports here

''' -- imports from installed packages -- '''
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.views.generic import RedirectView
from gnowsys_ndf.ndf.views.methods import get_execution_time
from gnowsys_ndf.ndf.views.analytics import *

try:
    from bson import ObjectId
except ImportError:  # old pymongo
    from pymongo.objectid import ObjectId

''' -- imports from application folders/files -- '''
from verc.settings import GAPPS, GSTUDIO_SITE_LANDING_PAGE, GSTUDIO_SITE_NAME, GSTUDIO_SITE_LANDING_TEMPLATE, GSTUDIO_OER_GROUPS
from verc.ndf.models import GSystemType, Node
from verc.ndf.models import node_collection
from verc.ndf.gstudio_es.es import *
from verc.ndf.gstudio_es.paginator import Paginator ,EmptyPage, PageNotAnInteger

###################################################
#   V I E W S   D E F I N E D   F O R   H O M E   #
###################################################
index = 'nodes'
print "in home.py"
#@get_execution_time
def homepage(request, group_id):
    print "Entered home.py"
    #print request,"\n"
    print request.user,"\n"
    print request.author
    if request.user.is_authenticated():
        # auth_gst = node_collection.one({'_type': u'GSystemType', 'name': u'Author'})
        # if auth_obj:
        #     auth_type = auth_obj._id
        # auth = node_collection.one({'_type': u"Author", 'created_by': int(request.user.id)})
        print "user name:",request.user.id

        q = eval("Q('bool', must=[Q('match', type = 'Author'), Q('match',created_by=int(request.user.id))])")

        # q = Q('match',name=dict(query='File',type='phrase'))
        auth1 = Search(using=es, index=index,doc_type="node").query(q)
        auth2 = auth1.execute()
        print "auth1:",auth2
        auth = auth2[0]
        # This will create user document in Author collection to behave user as a group.

        print GSTUDIO_SITE_LANDING_PAGE, request.user.id
        if GSTUDIO_SITE_LANDING_PAGE == "home":
            print "before reverse"
            return HttpResponseRedirect( reverse('e-library'), kwargs={"group_id": group_id} )

        else:
            return HttpResponseRedirect( reverse('dashboard', kwargs={"group_id": request.user.id}) )

    else:
        print "in home:",group_id,GSTUDIO_SITE_LANDING_PAGE
        if GSTUDIO_SITE_LANDING_PAGE == "home":
            return HttpResponseRedirect(  reverse('e-library', kwargs={"group_id": group_id} ) )

        else:
            return HttpResponseRedirect( reverse('groupchange', kwargs={"group_id": group_id}) )

#@get_execution_time
def landing_page(request):
    '''
    Method to render landing page after checking variables in local_settings/settings file.
    '''
    # group_id = node_collection.one({'$and':[{'_type': u'Group'}, {'name': u'home'}]})._id
    q = eval("Q('bool', must=[Q('match', type = 'Group'), Q('match',name='home')])")
    print "in landingpage"
    # q = Q('match',name=dict(query='File',type='phrase'))
    grp_id1 = Search(using=es, index=index,doc_type="node").query(q)
    grp_id2 = grp_id1.execute()
    print "response:",grp_id2
    group_id = grp_id2[0].id
    print GSTUDIO_SITE_NAME, GSTUDIO_SITE_LANDING_PAGE, GSTUDIO_SITE_LANDING_TEMPLATE

    if (GSTUDIO_SITE_LANDING_PAGE == "home") and (GSTUDIO_SITE_NAME == "NROER"):
        return render_to_response(
                                "ndf/landing_page_nroer.html",
                                {
                                    "group_id": "home", 'groupid':"home",
                                    'landing_page': 'landing_page'
                                },
                                context_instance=RequestContext(request)
                            )

    elif GSTUDIO_SITE_LANDING_TEMPLATE:
        if GSTUDIO_SITE_NAME == "clix":
            #print request.COOKIES
            
            if request.META['QUERY_STRING']  == "True":
                return render_to_response(
                                        GSTUDIO_SITE_LANDING_TEMPLATE,
                                        {
                                            "group_id": group_id, 'groupid':"home",
                                            'title': 'CLIx'
                                        },
                                        context_instance=RequestContext(request)
                                    )
            elif request.user.id:
                print "post loggin in"
                return HttpResponseRedirect( reverse('my_desk', kwargs={"group_id": request.user.id}) )        
            else:
                #print "Not yet logged in"
                group_id = node_collection.one({'_type': "Group", 'name': "home"})._id
                print request.path, request.META
                return HTTPResponse("Welcome" )
    else:
        return HttpResponseRedirect( reverse('groupchange', kwargs={"group_id": "home"}) )


# This class overrides the django's default RedirectView class and allows us to redirect it into user group after user logsin   
# class HomeRedirectView(RedirectView):
#     pattern_name = 'home'

#     def get_redirect_url(self, *args, **kwargs):
#       if self.request.user.is_authenticated():
#             auth_obj = node_collection.one({'_type': u'GSystemType', 'name': u'Author'})
#             if auth_obj:
#                 auth_type = auth_obj._id
#             auth = ""
#             auth = node_collection.one({'_type': u"Author", 'name': unicode(self.request.user)})
#             # This will create user document in Author collection to behave user as a group.

#             if auth is None:
#                 auth = node_collection.collection.Author()

#                 auth.name = unicode(self.request.user)
#                 auth.email = unicode(self.request.user.email)
#                 auth.password = u""
#                 auth.member_of.append(auth_type)
#                 auth.group_type = u"PUBLIC"
#                 auth.edit_policy = u"NON_EDITABLE"
#                 auth.subscription_policy = u"OPEN"
#                 user_id = int(self.request.user.pk)
#                 auth.created_by = user_id
#                 auth.modified_by = user_id
#                 if user_id not in auth.contributors:
#                     auth.contributors.append(user_id)
#                 # Get group_type and group_affiliation stored in node_holder for this author 
#                 try:
#                     temp_details = node_collection.one({'_type': 'node_holder', 'details_to_hold.node_type': 'Author', 'details_to_hold.userid': user_id})
#                     if temp_details:
#                         auth.agency_type=temp_details.details_to_hold['agency_type']
#                         auth.group_affiliation=temp_details.details_to_hold['group_affiliation']
#                 except e as Exception:
#                     print "error in getting node_holder details for an author"+str(e)
#                 auth.save()
                
#             # This will return a string in url as username and allows us to redirect into user group as soon as user logsin.
#             #return "/{0}/".format(auth.pk)
#             if GSTUDIO_SITE_LANDING_PAGE == 'home':
#                 #return "/home/dashboard/group"
#                 return "/home/"
#             else:    
#                 return "/{0}/dashboard".format(self.request.user.id)     
#         else:
#             # If user is not loggedin it will redirect to home as our base group.
#             #return "/home/dashboard/group"
#             return "/home/"
'''
@get_execution_time
def help_page_view(request,page_name):
    # page_obj = Node.get_node_by_id(page_id)
    # help_grp = node_collection.one({'$and':[{'_type': u'Group'}, {'name': u'help'}]})
    
    # page_obj = node_collection.one({"name":unicode(page_name),"group_set":ObjectId(help_grp._id)})
    print "in help page click"
    q = eval("Q('bool', must=[Q('match', type = 'Group'), Q('match',name='help')])")

    # q = Q('match',name=dict(query='File',type='phrase'))
    help_grp1 = Search(using=es, index=index,doc_type="node").query(q)
    help_grp2 = help_grp1.execute()
    help_grp = help_grp2[0]

    q = eval("Q('bool', must=[Q('match',name=page_name),Q('match', group_set = help_grp.id)])")
    page_obj2 = page_obj1.execute()
    page_obj = page_obj2[0]


    return render_to_response(
                                        "ndf/help_page.html",
                                        {
                                            "group_id": page_obj.id,
                                            'title': 'Help Page',
                                            'page_obj':page_obj
                                        },
                                        context_instance=RequestContext(request)
                                    )
'''
