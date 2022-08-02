''' -- imports from python libraries -- '''
# import os -- Keep such imports here

''' -- imports from installed packages -- '''
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template import RequestContext
from django.views.generic import RedirectView

try:
    from bson import ObjectId
except ImportError:  # old pymongo
    from pymongo.objectid import ObjectId

''' -- imports from application folders/files -- '''
from verc.settings import GAPPS, GSTUDIO_SITE_LANDING_PAGE, GSTUDIO_SITE_NAME, GSTUDIO_SITE_LANDING_TEMPLATE, GSTUDIO_OER_GROUPS
from ndf.models import GSystemType, Node
from ndf.models import node_collection
from ndf.gstudio_es.es import *
from ndf.gstudio_es.paginator import Paginator ,EmptyPage, PageNotAnInteger

###################################################
#   V I E W S   D E F I N E D   F O R   H O M E   #
###################################################
index = 'nodes'
#@get_execution_time
def homepage(request, group_id):
    print("Entered home.py")
    #print request,"\n"
    print(request.user)
    if request.user.is_authenticated:
        # auth_gst = node_collection.one({'_type': u'GSystemType', 'name': u'Author'})
        # if auth_obj:
        #     auth_type = auth_obj._id
        # auth = node_collection.one({'_type': u"Author", 'created_by': int(request.user.id)})
        print("user name:",request.user.id)

        q = eval("Q('bool', must=[Q('match', type = 'Author'), Q('match',created_by=int(request.user.id))])")

        # q = Q('match',name=dict(query='File',type='phrase'))
        auth1 = Search(using=es, index=index,doc_type="node").query(q)
        auth2 = auth1.execute()
        print("auth1:",auth2)
        auth = auth2[0]
        # This will create user document in Author collection to behave user as a group.

        print(GSTUDIO_SITE_LANDING_PAGE, request.user.id)
        if GSTUDIO_SITE_LANDING_PAGE == "home":
            print("before reverse")
            return HttpResponseRedirect( reverse('e-library'), kwargs={"group_id": group_id} )

        else:
            return HttpResponseRedirect( reverse('dashboard', kwargs={"group_id": request.user.id}) )

    else:
        print("in home:",group_id,GSTUDIO_SITE_LANDING_PAGE)
        if GSTUDIO_SITE_LANDING_PAGE == "home":
            return render(request,
                                        'index.html',
                                        {
                                            "group_id": group_id, 'groupid':"home",
                                            'title': 'CLIx'
                                        },
                                    )

        else:
            return HttpResponseRedirect( reverse('groupchange', kwargs={"group_id": group_id}) )

#@get_execution_time
def landing_page(request):
    '''
    Method to render landing page after checking variables in local_settings/settings file.
    '''
    # group_id = node_collection.one({'$and':[{'_type': u'Group'}, {'name': u'home'}]})._id
    q = eval("Q('bool', must=[Q('match', type = 'Group'), Q('match',name='home')])")
    print("in landingpage")
    # q = Q('match',name=dict(query='File',type='phrase'))
    grp_id1 = Search(using=es, index=index,doc_type="node").query(q)
    grp_id2 = grp_id1.execute()
    print("response:",grp_id2)
    group_id = grp_id2[0].id

    if GSTUDIO_SITE_LANDING_TEMPLATE:
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
                print("post loggin in")
                return HttpResponseRedirect( reverse('my_desk', kwargs={"group_id": request.user.id}) )        
            else:
                #print "Not yet logged in"
                group_id = node_collection.one({'_type': "Group", 'name': "home"})._id
                print(request.path, request.META)
                return HTTPResponse("Welcome" )
    else:
        return HttpResponseRedirect( reverse('groupchange', kwargs={"group_id": "home"}) )

