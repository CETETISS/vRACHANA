import re
import urllib
import json
import datetime
''' -- imports from installed packages -- '''
from django.shortcuts import render
from django.template import RequestContext
from ndf.gstudio_es.paginator import Paginator ,EmptyPage, PageNotAnInteger


try:
	from bson import ObjectId
except ImportError:  # old pymongo
	from pymongo.objectid import ObjectId

''' -- imports from application folders/files -- '''
from verc.settings import GAPPS
# from gnowsys_ndf.ndf.models import Node, GRelation,GSystemType,File,Triple
from ndf.models import Node, GRelation,GSystemType, Triple, hit_counter
from ndf.models import node_collection
#from gnowsys_ndf.ndf.views.file import *
#from gnowsys_ndf.ndf.views.methods import cast_to_data_type
from ndf.views.es_queries import get_node_by_id,get_group_name_id,get_nodes_by_ids_list,get_attribute_value
#from gnowsys_ndf.ndf.views.methods import get_filter_querydict
from ndf.gstudio_es.es import *
from elasticsearch_dsl import *
##############################################################################
print("elasticsearch client",es)
index = 'nodes'
doc_type = 'node'

# GST_FILE = node_collection.one({'_type':'GSystemType', 'name': "File"})

q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='File')])")
GST_FILE = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()

q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='Page')])")
GST_PAGE = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()

q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name=GAPPS[3])])")
GST_IMAGE = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()

# GST_IMAGE = node_collection.one({'_type':'GSystemType', 'name': GAPPS[3]})

q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name=GAPPS[4])])")
GST_VIDEO = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()

# GST_VIDEO = node_collection.one({'_type':'GSystemType', 'name': GAPPS[4]})
# e_library_GST = node_collection.one({'_type':'GSystemType', 'name': 'E-Library'})
q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='E-Library')])")
e_library_GST = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()

q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='Pandora_video')])")
pandora_video_st = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()
# pandora_video_st = node_collection.one({'_type':'GSystemType', 'name': 'Pandora_video'})

q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='Pandora_video')])")
app = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()

q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='Wiki page')])")
wiki_page = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()
# wiki_page = node_collection.one({'_type': 'GSystemType', 'name': 'Wiki page'})

q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='Jsmol')])")
GST_JSMOL = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()
# GST_JSMOL = node_collection.one({"_type":"GSystemType","name":"Jsmol"})

q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='Module')])")
gst_module = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()

#banner_pics = ['/static/ndf/Website Banners/About/About2.png','/static/ndf/Website Banners/Landing Page/elibrary1.png','/static/ndf/Website Banners/Landing Page/elibrary2.png','/static/ndf/elibrary 6.1.png','/static/ndf/Website Banners/Landing Page/elibrary4.png','/static/ndf/Website Banners/Landing Page/elibrary5.png','/static/ndf/Website Banners/Landing Page/elibrary6.png']


banner_pics = ['/static/ndf/Website Banners/Landing Page/Revised-eLibrary/e-Library-1_mod.jpg','/static/ndf/Website Banners/Landing Page/Revised-eLibrary/eLibrary-2.png','/static/ndf/Website Banners/Landing Page/Revised-eLibrary/eLibrary-3.jpg','/static/ndf/Website Banners/Landing Page/Revised-eLibrary/elib-7_mod.png','/static/ndf/Website Banners/Landing Page/Revised-eLibrary/e-Library-5_mod.png','/static/ndf/Website Banners/Landing Page/Revised-eLibrary/eLibrary-6.jpg','/static/ndf/Website Banners/COOL-website-slider/COOL_website_Banner_latest.png']

##############################################################################


def resource_list(request, groupid, app_id=None, page_no=1):
        print("inside resource_list of e-library ",groupid)
        is_video = request.GET.get('is_video', "")
        lang = request.LANGUAGE_CODE
        print("request:",request.session.get_expiry_age(),request.session.get_expire_at_browser_close())
        print("language data from request:",lang,request.session)
        try:
                group_id = ObjectId(groupid)
        except:
                group_name, group_id = get_group_name_id(groupid)

        print("group name and id", group_id)
        if app_id is None:
                app_id = str(app[0].id)
        title = e_library_GST[0].name
        file_id = GST_FILE[0].id
        datavisual = []
        no_of_objs_pp = 5
        query_dict = []
	# query_dict = filters
        selfilters = urllib.parse.unquote(request.GET.get('selfilters', ''))
        if selfilters:
                print("post fetching filters",selfilters)
                selfilters = json.loads(selfilters)
                print("post json loads :", selfilters)
                query_dict = get_filter_querydict(selfilters)
        print("query dict",query_dict)
        lists = esearch.es_filters(query_dict)
        print("post esearch",lists)
        strconcat1 = ""
        for value in lists:
                strconcat1 = strconcat1+'eval(str("'+ value +'")),'
        
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id]),Q('match',group_set=str(group_id)),Q('match_phrase',language = lang),Q('match',access_policy='PUBLIC')],must_not=[Q('match',attribute_set__educationaluse='ebooks')])
        allfiles1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "desc"}})
        allfiles2 = allfiles1.execute()
        educationaluse_stats = {}
	#print "all_files:",allfiles1
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',group_set=str(group_id)),Q('match',access_policy='PUBLIC'),Q('match_phrase',if_file__mime_type = 'image')])
        allimages1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "desc"}})
        allimages2 = allimages1.execute()
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',group_set=str(group_id)),Q('match',access_policy='PUBLIC'),Q('match_phrase',if_file__mime_type = 'video')])
        allvideos1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "desc"}})
        allvideos2 = allvideos1.execute()
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',group_set=str(group_id)),Q('match',access_policy='PUBLIC'),Q('match_phrase',if_file__mime_type = 'audio')])
        allaudios1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "desc"}})
        allaudios2 = allaudios1.execute()
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',language = lang),Q('match_phrase',tags = 'Handbook')])
        alldocs1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "desc"}})
        alldocs2 = alldocs1.execute()
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',language = lang),Q('match_phrase',tags = 'Tool')])
        allinteractives1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({'last_update' : {"order":"asc"}})
        allinteractives2 = allinteractives1.execute()
        print("interactives count:",allinteractives1.count())
        
        domain_set = ['English','Mathematics','Science','Digital Literacy']
        domain_nds = [get_group_name_id(each)[1] for each in domain_set]
        domains = get_nodes_by_ids_list(domain_nds)
        moduleids = []
        english_mod_ids=[]
        for each in domains:
                if each.name == 'English':
                        english_mod_ids.extend(each.collection_set)
                moduleids.extend(each.collection_set)
        #moduleids.append('5a9ff13a69602a0156048cd6')
        print("moduleids:",moduleids,english_mod_ids)
        q1= Q('bool', must=[Q('match', member_of = gst_module[0].id), Q('match',status='PUBLISHED'),Q('terms',id = moduleids),Q('match_phrase',language = lang)])
        q2 = Q('bool',must=[Q('terms',id = english_mod_ids)])
        q3 = Q('bool',should=[q1,q2])
        all_modules = (Search(using=es,index = index,doc_type=doc_type).query(q3)).sort({"last_update" : {"order" : "asc"}})
        all_modules2 = all_modules.execute()
        print("modules:",all_modules.count())
        files_new = all_modules[0:24]
        datavisual.append({"name":"Doc", "count": alldocs1.count()})
        datavisual.append({"name":"Page", "count": educationaluse_stats.get("Pages", 0)})
        datavisual.append({"name":"Image","count": allimages1.count()})
        datavisual.append({"name":"Video","count": allvideos1.count()})
        datavisual.append({"name":"Interactives","count": allinteractives1.count()})
        datavisual.append({"name":"Audios","count": allaudios1.count()})
        datavisual.append({"name":"eBooks","count": educationaluse_stats.get("eBooks", 0)})
        if 'sessionid' in request.COOKIES.keys():
                print("Session:",request.COOKIES['sessionid'])
                results = hit_counter.objects.filter(session_id=request.COOKIES['sessionid'],visitednode_name='home')
                print("values:",request.COOKIES['sessionid'],group_id,'home',datetime.now())
                if len(results) ==0:
                        obj = hit_counter.objects.create(session_id=request.COOKIES['sessionid'],visitednode_id=group_id,visitednode_name='home',preview_count=0,visit_count=1,download_count=0,created_date=datetime.now(),last_updated=datetime.now())
                        obj.save()
        #else:
                #cnt = results[0].visit_count
                #obj1 = results[0]
                #obj1.visit_count += 1
                #obj1.save()
        q = Q('bool',must=[Q('match',access_policy='PUBLIC'), Q('match_phrase',tags='unplatform-exe')])
        allpckgs = {}
        all_pckgs = (Search(using=es,index = index,doc_type=doc_type).query(q))
        all_pckgs1 = all_pckgs.execute()
        for each in all_pckgs1[0:all_pckgs.count()]:
                print("tags:",each.tags)
                if each.tags[0].find('english') > 0:
                        allpckgs['English-'+each.language[0]] = each.if_file.original.relurl
                elif each.tags[0].find('mathematics') > 0:
                        allpckgs['Mathematics-'+each.language[0]] = each.if_file.original.relurl #each.if_file.original.relurl
                else:
                        allpckgs['Science-'+each.language[0]] = each.if_file.original.relurl #each.if_file.original.relurl
        print("pckg urls:",allpckgs,groupid,group_id)
        return render(request,"ndf/Elibrary.html", {'title': title, 'app':e_library_GST[0],'appId':app[0].id, "app_gst": app[0],'files': files_new,'detail_urlname': "file_detail",'ebook_pages': educationaluse_stats.get("eBooks", 0),'file_pages':all_modules.count(),'interactive_pages':allinteractives1.count(),'image_pages': allimages1.count(),'educationaluse_stats': json.dumps(educationaluse_stats),'doc_pages': alldocs1.count(),'video_pages': allvideos1.count(),'audio_pages': allaudios1.count(),'groupid': groupid, 'group_id':group_id,"datavisual":datavisual, 'bannerpics': banner_pics,'allpckgs':allpckgs,'lang':request.LANGUAGE_CODE})


#@get_execution_time
def elib_paged_file_objs(request, groupid, filetype, page_no):
        print("in elib_paged_file_objs",request.is_ajax(),request.method)
        domain_name = request.POST.getlist("domain_name")
        domain_selected = request.POST.getlist("domain_selected")
        lang = request.LANGUAGE_CODE
        if request.is_ajax() and request.method == "POST":
                if len(domain_selected) == 0:
                        group_name, group_id = get_group_name_id(groupid)               
                        no_of_objs_pp = 5
                        result_pages = None
                        filetype = filetype.lower()
                        #print "filetype received:",filetype
                        detail_urlname = "file_detail"
                        template = 'ndf/module_cards.html'
                        if filetype != 'module':
                                if filetype == 'document':
                                        template = 'ndf/player_handbook.html'
                                        #print "in Document elif"
                                        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',tags = 'Handbook'),Q('match_phrase',language = lang)])
                                elif filetype == 'interactives':
                                        #print "in interactives"
                                        template = "ndf/player_interactive.html"
                                        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',tags = 'Tool'),Q('match_phrase',language = lang)])
                                else:
                                        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',group_set=str(group_id)),Q('match',access_policy='PUBLIC'),Q('match_phrase',if_file__mime_type = filetype),Q('match_phrase',language = lang)])
                        else:
                                domain_set = ['English','Mathematics','Science','Digital Literacy']
                                domain_nds = [get_group_name_id(each)[1] for each in domain_set]
                                domains = get_nodes_by_ids_list(domain_nds)
                                moduleids = []
                                english_mod_ids = []
                                for each in domains:
                                        if each.name == 'English':
                                                english_mod_ids.extend(each.collection_set)
                                        moduleids.extend(each.collection_set)
                                        #print "moduleids:", moduleids,english_mod_ids
                                q1= Q('bool', must=[Q('match', member_of = gst_module[0].id), Q('match',status='PUBLISHED'),Q('terms',id = moduleids),Q('match_phrase',language = lang)])
                                q2 = Q('bool',must=[Q('terms',id = english_mod_ids)])
                                q = Q('bool',should=[q1,q2])
                        allfiletypes1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "asc"}})
                        allfiletypes2 = allfiletypes1.execute()
                       
                else:
                        group_name, group_id = get_group_name_id(groupid)
                        no_of_objs_pp = 5
                        result_pages = None
                        filetype = filetype.lower()
                        #print "filetype received:",filetype
                        detail_urlname = "file_detail"
                        template = 'ndf/module_cards.html'
                        domain_nds = []
                        for each in domain_selected:
                                domain_name,domain_id = get_group_name_id(each)
                                nd = get_node_by_id(domain_id)
                                domain_nds.append(nd)
                        #print "domain nds:",domain_nds
                        unitnds = []
                        modules = []
                        eng_mods = []
                        for eachnd in domain_nds:
                                if eachnd.name == 'English':
                                        eng_mods.extend(eachnd.collection_set)
                                modulends = get_nodes_by_ids_list(eachnd.collection_set)
                                for eachmod in modulends:
                                        modules.append(eachmod.id)
                                        unitnds.extend(eachmod.collection_set)
                        #print "final grp_set:",unitnds
                        if filetype != 'module':
                                if filetype == 'document':
                                        template = 'ndf/player_handbook.html'
                                        #print "in Document elif"
                                        domain_selected = [str(each).title() for each in domain_selected]
                                        #print "domain selected:",domain_selected
                                        q1 = []
                                        for each in domain_selected:
                                                q1.append(Q('match_phrase',tags = str(each)))
                                        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',tags = 'Handbook'), Q('match_phrase',language = lang)],should = q1,minimum_should_match=1)
                                elif filetype == 'interactives':
                                        template = "ndf/player_interactive.html"
                                        domain_selected = [str(each).title() for each in domain_selected]
                                        #print "domain selected:",domain_selected
                                        q1 = []
                                        for each in domain_selected:
                                                q1.append(Q('match_phrase',tags = str(each)))
                                        #print q1
                                        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',tags = 'Tool'),Q('match_phrase',language = lang)],should=q1,minimum_should_match=1)
                                else:
                                        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',group_set=str(group_id)),Q('match',access_policy='PUBLIC'),Q('match_phrase',if_file__mime_type = filetype),Q('terms',group_set = unitsnds),Q('match_phrase',language = lang)])
                        else:
                                #print "module ids",modules
                                q1= Q('bool', must=[Q('match', member_of = gst_module[0].id),Q('terms',id = modules),Q('match_phrase',language = lang),Q('match',status='PUBLISHED')])
                                if eng_mods:
                                        q2 = Q('bool',must=[Q('terms',id = eng_mods)])
                                        q = Q('bool',should=[q1,q2])
                                else:
                                        q = q1
                        allfiletypes1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "asc"}})
                        allfiletypes2 = allfiletypes1.execute()
                educationaluse_stats = {}
                #print "allfiletypes:", allfiletypes1.count()                                                                                                          
                files_new = allfiletypes1[0:allfiletypes1.count()]
                if files_new:
                        eu_list = []  # count                                                                                                                   
                        collection_set_count = 0       
                        if set(eu_list):
                                if len(set(eu_list)) > 1:
                                        educationaluse_stats = dict((x, eu_list.count(x)) for x in set(eu_list))
                                elif len(set(eu_list)) == 1:
                                        educationaluse_stats = { eu_list[0]: eu_list.count(eu_list[0])}
                                        educationaluse_stats["all"] = files.count()
                                        educationaluse_stats["Collections"] = collection_set_count
                                        
                filter_result = "True" if (allfiletypes1.count() > 0) else "False"
                #print "template",template
                with open('/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/ndf/static/ndf/theInteractive.json','r') as json_file:
                        interactivedata = json.load(json_file)
                
                return render (request,template, {
				"filter_result": filter_result,
				"group_id": group_id, "group_name_tag": group_id, "groupid": group_id,
				'title': "E-Library", "educationaluse_stats": json.dumps(educationaluse_stats),
				"files": allfiletypes1[0:allfiletypes1.count()], "detail_urlname": detail_urlname,
			        "filetype": filetype, "res_type_name": "","interactivedata":interactivedata, 'bannerpics': banner_pics
			})


def resource_list_domainwise(request,groupid, app_id=None, page_no=1):
        """
        * Renders a list of all 'Resources' available within the database (except eBooks).
        """
        #print "home group id:",group_id
        lang = request.LANGUAGE_CODE
        domain_name = request.POST.getlist("domain_name")
        #print "inside resource_list_domainwise of e-library ",domain_name
        try:
                group_id = ObjectId(groupid)
        except:
                group_name, group_id = get_group_name_id(groupid)
        #print "group name and id",group_id
        domain_set = []
        if len(domain_name) == 0:
                domain_name = ['English','Mathematics','Science','Digital Literacy']
        if len(domain_name) > 1:
                for each in domain_name:
                        #print "each val:",each
                        domain_group_name, domain_group_id = get_group_name_id(each)
                        domain_set.append(domain_group_id)
        
        else:
                if len(domain_name) ==1:
                        if 'All' == domain_name[0]:
                                domain_set.append(group_id)
                        else:
                                domain_group_name, domain_group_id = get_group_name_id(domain_name[0])
                                domain_set.append(domain_group_id)

        #print "domain set:",domain_set
        domainds = get_nodes_by_ids_list(domain_set)
        #print "domain nds:",domainds
        idlist = []
        eng_mods = []
        for each in domainds:
                if each.name == 'English':
                        eng_mods.extend(each.collection_set)
                idlist.extend(each.collection_set)
        #print "modules:",idlist
        idnds = get_nodes_by_ids_list(idlist)
        unitslist = []
        for each in idnds:
                unitslist.extend(each.collection_set)
        #print "units:",unitslist
        if app_id is None:
                app_id = str(app[0].id)
        title = e_library_GST[0].name
        file_id = GST_FILE[0].id
        datavisual = []
        no_of_objs_pp = 5
        domain_set = [str(each) for each in domain_set]
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id]),Q('terms',group_set=domain_set),Q('match',access_policy='PUBLIC'),Q('match_phrase',language = lang)],must_not=[Q('match',attribute_set__educationaluse='ebooks')])
        allfiles1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "desc"}})
        allfiles2 = allfiles1.execute()
        educationaluse_stats = {}
        #print "all_files:",allfiles1

        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('terms',group_set=domain_set),Q('match',access_policy='PUBLIC'),Q('match_phrase',if_file__mime_type = 'image')])
        allimages1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "desc"}})
        allimages2 = allimages1.execute()
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('terms',group_set=domain_set),Q('match',access_policy='PUBLIC'),Q('match_phrase',if_file__mime_type = 'video')])
        allvideos1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "desc"}})
        allvideos2 = allvideos1.execute()

        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('terms',group_set=domain_set),Q('match',access_policy='PUBLIC'),Q('match_phrase',if_file__mime_type = 'audio')])
        allaudios1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "desc"}})
        allaudios2 = allaudios1.execute()
        q1 = []
        for each in domain_name:
                q1.append(Q('match_phrase',tags = str(each)))
        #print q1
                                        
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match_phrase',tags = 'Handbook'),Q('match_phrase',language = lang)],should = q1,minimum_should_match=1)
        alldocs1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "desc"}})
        alldocs2 = alldocs1.execute()
        q1= Q('bool', must=[Q('match', member_of = gst_module[0].id), Q('match',status='PUBLISHED'),Q('terms',id=idlist),Q('match_phrase',language = lang)])
        if eng_mods:
                q2 = Q('bool',must=[Q('terms',id = eng_mods)])
                q = Q('bool',should=[q1,q2])
        else:
                q = q1

        all_modules = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "asc"}})

        all_modules2 = all_modules.execute()

        if len(domain_name) == 0:
                domain_name = ['Science','Mathematics','English']
        q1 = []
        for each in domain_name:
                q1.append(Q('match_phrase',tags = str(each)))
        #print q1
        
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',tags = 'Tool'),Q('match_phrase',language = lang)],should=q1,minimum_should_match=1)
       
        #print "interactive query:",q
        all_interactives1 = (Search(using=es,index = index,doc_type=doc_type).query(q))
        all_interactives2 = all_interactives1.execute()
        #print "interactives count:",all_interactives1.count()
        #print "query",q
        files_new = all_modules[0:all_modules.count()]
        datavisual.append({"name":"Doc", "count": alldocs1.count()})
        datavisual.append({"name":"Page", "count": educationaluse_stats.get("Pages", 0)})
        datavisual.append({"name":"Image","count": allimages1.count()})
        datavisual.append({"name":"Video","count": allvideos1.count()})
        datavisual.append({"name":"Interactives","count": all_interactives1.count()})
        datavisual.append({"name":"Audios","count": allaudios1.count()})
        datavisual.append({"name":"eBooks","count": educationaluse_stats.get("eBooks", 0)})

        #print "educational stats:",educationaluse_stats,all_modules2
        response = render(request,"ndf/theE.html",
                                  {'title': title, 'app':e_library_GST[0],
                                   'appId':app[0].id, "app_gst": app[0],
                                   # 'already_uploaded': already_uploaded,'shelf_list': shelf_list,'shelves': shelves,
                                   'files': files_new,
                                   'file_pages':all_modules.count(),
                                   "detail_urlname": "file_detail",
                                   'ebook_pages': educationaluse_stats.get("eBooks", 0),
                                   'image_pages': allimages1.count(),
                                   'interactive_pages': all_interactives1.count(),
                                   'educationaluse_stats': json.dumps(educationaluse_stats),
                                   'doc_pages': alldocs1.count(),
                                   'video_pages': allvideos1.count(),
                                   'audio_pages': allaudios1.count(),
                                   'groupid': group_id,'group_name_tag':group_id, 'group_id':group_id,
                                   "datavisual":datavisual,'bannerpics': banner_pics
                           })
        
        for each in ['English','Mathematics','Science']:
                print("each value:",each)
                if( each in domain_name):
                        response.set_cookie(each,True)
                else:
                        response.set_cookie(each,False)
        return response
