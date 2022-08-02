
import datetime
import time
import subprocess
import re
import ast
import string
import json
import locale
from sys import getsizeof, exc_info
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.urls import reverse
from django.shortcuts import render_to_response , render
from django.template.loader import render_to_string

from django.template import RequestContext
from django.template.defaultfilters import slugify
from ndf.gstudio_es.paginator import Paginator ,EmptyPage, PageNotAnInteger

from django.core.cache import cache
from bson import ObjectId
from ndf.gstudio_es.es import *
from elasticsearch_dsl import *
from verc.settings import GSTUDIO_SITE_LANDING_PAGE,LANGUAGES,EMAIL_HOST_USER,GSTUDIO_RESOURCES_LANGUAGES,GSTUDIO_RESOURCES_EDUCATIONAL_SUBJECT,GSTUDIO_RESOURCES_EDUCATIONAL_LEVEL
from django.shortcuts import render_to_response
from django.template import RequestContext
from ndf.models import GSystemType, Group, Node, GSystem, Author, hit_counter  #, Triple
from ndf.models import node_collection,triple_collection

from ndf.models import GSystemType

def test_session(request):
    request.session.set_test_cookie()
    return HttpResponse("Testing session cookie")


def test_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("Cookie test passed")
    else:
        response = HttpResponse("Cookie test failed")
    return response

gfs = HashFS('/data/media/', depth=3, width=1, algorithm='sha256')

banner_pics1 = ['/static/ndf/Website Banners/Landing Page/Revised_imgs/e-Library-1_mod.jpg','/static/ndf/Website Banners/Landing Page/elibrary2.png','/static/ndf/elibrary 6.1.png','/static/ndf/Website Banners/Landing Page/elibrary4.png','/static/ndf/Website Banners/Landing Page/Revised_imgs/e-Library-5_mod.png','/static/ndf/Website Banners/Landing Page/elibrary6.png','/static/ndf/Website Banners/COOL-website-slider/COOL_website_Banner_latest.png']

trans_rel_type = '5752ad572e01310a05dca50f'
#language = {'en':0,'te':0,'ta':0,'pu':0,'ma':0,'hi':0}
def cool_resourcelist(request):
    language = {'en':0,'te':0,'ta':0,'pu':0,'ma':0,'hi':0}
    subject = {'Science':0,'Mathematics':0,'art':0,'language':0,'MultipleSubjects':0}
    rsrc_type = {'Hands_On':0,'Simulation':0,'Tool':0,'Forum':0}
    level = {'K-12':0,'6-12':0}
    banner_pics1 = ['/static/ndf/OER_1200_300_Slider_1.jpg','/static/ndf/OER_1200_300_Slider_2.jpg','/static/ndf/OER_1200_300_Slider_3.jpg','/static/ndf/OER_1200_300_Slider_4.jpg','/static/ndf/OER_1200_300_Slider_5.jpg','/static/ndf/Website Banners/COOL-website-slider/COOL_website_Banner_latest.png']
    print("in cool resource list")
    index = 'nodes'
    doc_type = 'node'
    q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='cool_resource')])")
    gst_cool_resource = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()
    dt = {u'knowledge_theme': u'Knowledge deepening'}
    q = Q('bool',must=[Q('terms',member_of=[gst_cool_resource[0].id]),Q('match',status='PUBLISHED'),Q('match',access_policy='PUBLIC')])
    cooloers1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "asc"}})
    cooloers2 = cooloers1.execute()
    koers=[]
    coers=[]
    toers = []
    for each in cooloers1[0:cooloers1.count()]:
        #print each.attribute_set
        l = list(each.attribute_set)
        d = {k:v for element in l for k,v in element.to_dict().items()}
        if 'knowledge_theme' in d:
            if d['knowledge_theme']=='Knowledge deepening':
                koers.append(each)
            elif d['knowledge_theme']=='Creativity and 21st century skills':
                coers.append(each)
            else:
                toers.append(each)
    #print "knowledge oers:", koers
    koers.sort(key=lambda x: x.name, reverse=False)
    coers.sort(key=lambda x: x.name, reverse=False)
    toers.sort(key=lambda x: x.name, reverse=False)
    get_all_counts(koers,coers,toers,language,subject,level,rsrc_type)
    '''q = Q('bool',must=[Q('terms',member_of=[gst_cool_resource[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',tags='Creativity')])
    cooloers1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "asc"}})
    cooloers2 = cooloers1.execute()
    coers = cooloers1[0:cooloers1.count()]

    q = Q('bool',must=[Q('terms',member_of=[gst_cool_resource[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',tags='Tinkering')])
    cooloers1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "asc"}})
    cooloers2 = OAcooloers1.execute()
    toers = cooloers1[0:cooloers1.count()]
'''
    q = Q('match', name = 'home')
    s1 = Search(using=es, index='nodes',doc_type="node").query(q)
    s2 = s1.execute()
    if 'sessionid' in request.COOKIES.keys():
        results = hit_counter.objects.filter(session_id=request.COOKIES['sessionid']).filter(visitednode_name='COOL-OER')
        if len(results) ==0:
            obj = hit_counter.objects.create(session_id=request.COOKIES['sessionid'],visitednode_id=s2[0].id,visitednode_name='COOL-OER',preview_count=0,visit_count=1,download_count=0,created_date=datetime.now(),last_updated=datetime.now())
            obj.save()
            print("hit_counter object saved")
        else:
            obj1 = results[0]
            #print "else:",obj1.visitednode_name,obj1.visit_count                                                                                                      
            if obj1.visit_count == 0:
                obj1.visit_count = 1
                obj1.save()
            else:
                obj1.visit_count += 1
                obj1.save()

    print(subject,level,rsrc_type)
    with open('/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/ndf/static/ndf/cool_resources_details.json','r',encoding='utf-8') as json_file:
                        coolresourcedata = json.load(json_file)
  
    return render(request,"ndf/TheCOOL_OER.html",{
                                    'title':'COOL-OER','coolresourcedata':coolresourcedata,'groupid':'home','group_id':'home','bannerpics':banner_pics1,'k_oers':koers,'koers_count':len(koers),'c_oers':coers,'coers_count':len(coers),'t_oers':toers,'toers_count':len(toers),'lang':language,'subjt':subject,'grade':level,'rsrc':rsrc_type
})

def get_tran_nodes(subject,rel_type,lang):
    q = Q('bool',must = [Q('match',subject = subject),Q('match',type= 'GRelation'),Q('match', relation_type= rel_type)]) 
    s1 = Search(using=es, index='triples',doc_type="triple").query(q)
    res = s1.execute()
    nds = []
    for each in s1:
        print("in trans nodes:",s1.count())
        nd = get_node_by_id(each.right_subject)
        if len(lang) > 0:
            if any(x in lang for x in nd.language):
                nds.append(nd)
        else:
            nds.append(nd)
    if len(lang) != 0 and not 'en' in lang:
        for each in nds:
            print("lang:",each.language, 'en' in each.language)
            if 'en' in each.language:
                nds.pop(each)
    print("nds count:",len(nds))
    return nds

def get_all_counts(k_oers,c_oers,t_oers,language,subject,level,rsrc_type):
    print("in get_all count",subject,level,rsrc_type)
    for each in k_oers:
        #if 'en' in each.language:
        l = list(each.attribute_set)
        d = {k:v for element in l for k,v in element.to_dict().items()}
        fetch_counts(each,d,language,subject,level,rsrc_type)
        
    for each in c_oers:
        #if 'en' in each.language:
        l = list(each.attribute_set)
        d = {k:v for element in l for k,v in element.to_dict().items()}
        fetch_counts(each,d,language,subject,level,rsrc_type)
        
    for each in t_oers:
        #if 'en' in each.language:
        l = list(each.attribute_set)
        d = {k:v for element in l for k,v in element.to_dict().items()}
        fetch_counts(each,d,language,subject,level,rsrc_type)
        
def fetch_counts(oer,attrb_set,language,subject,level,rsrc_type):
    #language = {'en':0,'te':0,'ta':0,'pu':0,'ma':0,'hi':0}
    #subject = {'Science':0,'Mathematics':0,'art':0,'language':0,'MultipleSubjects':0}
    #rsrc_type = {'Hands_On':0,'Simulation':0,'Tool':0,'Forum':0}
    #grade = {'K-12':0,'6-12':0}
    if 'en' in oer.language:
        language['en'] += 1
    elif 'hi' in oer.language:
        language['hi'] += 1
    elif 'ta' in oer.language:
        language['ta'] += 1
    elif 'te' in oer.language:
        language['te'] += 1
    elif 'pu' in oer.language:
        language['pu'] += 1
    else:
        language['ma'] += 1
    
    print(level)

    if 'K-12' in attrb_set['educationallevel']:
        print("in k-12")
        level['K-12'] += 1
    else:# '6-12' in attrb_set['educationallevel']:
        print("in 6-12")
        level['6-12'] += 1


    if 'en' in oer.language:
        #q = Q('bool',must = [Q('match',subject = oer.id),Q('match',type= 'GRelation'),Q('match', relation_type= trans_rel_type)])
        #s1 = Search(using=es, index='triples',doc_type="triple").query(q)
        #res = s1.execute()
        #t_nds = get_tran_nodes(oer.id,trans_rel_type,['en','hi','ma','te','ta',)
        #print "in fetch count",oer.name,s1.count()
        if 'Multiple Subjects' in  attrb_set['educationalsubject']:
            subject['MultipleSubjects'] +=1
        if 'Mathematics' in attrb_set['educationalsubject']:
            subject['Mathematics'] +=1
        if 'Science' in attrb_set['educationalsubject']:
            subject['Science'] +=1
        if 'Art' in attrb_set['educationalsubject']:
            subject['art'] +=1
         #'language' in attrb_set['educationalsubject']:
        if 'Language' in attrb_set['educationalsubject']:
            subject['language'] +=1
        
        if 'Simulation' in  attrb_set['resource_type']:                                                                                                         
            rsrc_type['Simulation'] +=1 
        if 'Tool' in attrb_set['resource_type']:                                                                                                             
            rsrc_type['Tool'] +=1                                                                                                             
        if 'Forum' in attrb_set['resource_type']:                                                                                                                 
            rsrc_type['Forum'] +=1                                                                                                                    
        if 'Hands-on' in attrb_set['resource_type']: #'Hands On' in attrb_set['resource_type']:                                                                        
            rsrc_type['Hands_On'] +=1
    else:
        q = Q('bool',must = [Q('match',type= 'GRelation'),Q('match', relation_type= trans_rel_type)])                                     
        s1 = Search(using=es, index='triples',doc_type="triple").query(q)                                                                                             
        res = s1.execute()
        for each in s1[0:s1.count()]:
            if each.right_subject == oer.id:
                eng_id = each.subject
                eng_nd = get_node_by_id(eng_id)
                l = list(eng_nd.attribute_set)
                attrb_set = {k:v for element in l for k,v in element.to_dict().items()}
                if 'Multiple Subjects' in  attrb_set['educationalsubject']:
                    subject['MultipleSubjects'] +=1
                if 'Mathematics' in attrb_set['educationalsubject']:
                    subject['Mathematics'] +=1
                if 'Science' in attrb_set['educationalsubject']:
                    subject['Science'] +=1
                if 'Art' in attrb_set['educationalsubject']:
                    subject['art'] +=1
                    #'language' in attrb_set['educationalsubject']:                                                                                                    
                if 'Language' in attrb_set['educationalsubject']:
                    subject['language'] +=1
                if 'Simulation' in  attrb_set['resource_type']:
                    rsrc_type['Simulation'] +=1
                if 'Tool' in attrb_set['resource_type']:
                    rsrc_type['Tool'] +=1
                if 'Forum' in attrb_set['resource_type']:
                    rsrc_type['Forum'] +=1
                if 'Hands-on' in attrb_set['resource_type']: #'Hands On' in attrb_set['resource_type']:                                                                
                    rsrc_type['Hands_On'] +=1


def predicate(rsrc_type, subject, grade, oer):
    #def _predicate(oer):
    print("in predicate", rsrc_type,oer['resource_type'])
    subjs = [x.strip() for x in str(oer['educationalsubject']).split(',')]
    print(subjs)
    if not len(rsrc_type) == 0 and not any(x in str(oer['resource_type']).split(',') for x in rsrc_type):
        return False
    if not len(subject) == 0 and not any(x in subjs for x in subject):
        return False
    if not len(grade) ==0  and not any(x in oer['educationallevel'] for x in grade):
        return False
    return True
    #return _predicate

#my_filtered_fruit = list(filter(predicate(query_type, query_color, query_size), myfruits.items()))

def cool_resourcelist_filter(request):
    language = {'en':0,'te':0,'ta':0,'pu':0,'ma':0,'hi':0}
    subject = {'Science':0,'Mathematics':0,'art':0,'language':0,'MultipleSubjects':0}
    rsrc_type = {'Hands_On':0,'Simulation':0,'Tool':0,'Forum':0}
    level = {'K-12':0,'6-12':0}
    banner_pics1 = ['/static/ndf/OER_1200_300_Slider_1.jpg','/static/ndf/OER_1200_300_Slider_2.jpg','/static/ndf/OER_1200_300_Slider_3.jpg','/static/ndf/OER_1200_300_Slider_4.jpg','/static/ndf/OER_1200_300_Slider_5.jpg','/static/ndf/COOL_website_Banner_Banner_1200-300.png']
    print("in cool resource list filter")
    index = 'nodes'
    doc_type = 'node'
    grade = request.POST.getlist('Grade')
    subj = request.POST.getlist('subdomain')
    rsrc = request.POST.getlist('resourcetype')
    lang_support = request.POST.getlist('Language_support')
    l = request.POST.get('lang')
    import ast
    l = l.replace(" ","").replace("&#39;"," ").replace(" ","'")
    #print("l",l)
    l1 = ast.literal_eval(l)
    s = request.POST.get('subjt')
    s = s.replace(" ","").replace("&#39;"," ").replace(" ","'")
    s1 = ast.literal_eval(s)
    r = request.POST.get('rsrc')
    r = r.replace(" ","").replace("&#39;"," ").replace(" ","'")
    r1 = ast.literal_eval(r)
    g = request.POST.get('grde')
    g = g.replace(" ","").replace("&#39;"," ").replace(" ","'")
    g1 = ast.literal_eval(g)
    print("filter values",l,s,r,g)
    q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='cool_resource')])")
    gst_cool_resource = (Search(using=es,index = index,doc_type=doc_type).query(q)).execute()
    #dt = {u'knowledge_theme': u'Knowledge deepening'}
    q = Q('bool',must=[Q('terms',member_of=[gst_cool_resource[0].id]),Q('match',status='PUBLISHED'),Q('match',access_policy='PUBLIC'),Q('match_phrase',language='en')])
    cooloers1 = (Search(using=es,index = index,doc_type=doc_type).query(q)).sort({"last_update" : {"order" : "asc"}})
    cooloers2 = cooloers1.execute()
    print("coers count:",cooloers1.count())
    koers=[]
    coers=[]
    toers = []
    
   # trans_rel_type = '5752ad572e01310a05dca50f'
    if len(subj) !=0:
        subjs =','.join(subj)
        print(subjs,subj)
    for each in cooloers1[0:cooloers1.count()]:
        #print each.attribute_set
        l = list(each.attribute_set)
        d = {k:v for element in l for k,v in element.to_dict().items()}
        #print "dict of attributes",d
        if 'knowledge_theme' in d:
            subjt =str(d['educationalsubject']).split(',')
            if d['knowledge_theme']=='Knowledge deepening':
                '''
                if ((len(grade) != 0 and d['educationallevel'][0] in grade)) and if(len(rsrc) != 0 and d['resource_type'] in rsrc) and if (len(subj)!= 0 and any(x in subjt for x in subj)):
                    koers.append(each)
                    koers.extend(get_tran_nodes(each.id,trans_rel_type,lang_support))
                else:
                    if len(grade) == 0 and len(subj) == 0 and len(rsrc) == 0:
                        print "in else"'''
                if predicate(rsrc, subj, grade, d):
                        koers.append(each)
                        #k_trns_nds = []
                        koers.extend(get_tran_nodes(each.id,trans_rel_type,lang_support))
                        
            elif d['knowledge_theme']=='Creativity and 21st century skills':
                if predicate(rsrc, subj, grade, d):
                    coers.append(each)
                    coers.extend(get_tran_nodes(each.id,trans_rel_type,lang_support))
                    
            else:
                if predicate(rsrc, subj, grade, d):
                    toers.append(each)
                    toers.extend(get_tran_nodes(each.id,trans_rel_type,lang_support))
    
    if len(lang_support) != 0 and not 'en' in lang_support:
        koers = [each for each in koers if 'en' not in each.language]
        coers = [each for each in coers if 'en' not in each.language]
        toers = [each for each in toers if 'en' not in each.language]
    print("knowledge oers:", len(koers), len(coers), len(toers))
    koers.sort(key=lambda x: x.name, reverse=False)
    coers.sort(key=lambda x: x.name, reverse=False)
    toers.sort(key=lambda x: x.name, reverse=False)
    
    get_all_counts(koers,coers,toers,language,subject,level,rsrc_type)
    
    with open('/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/ndf/static/ndf/cool_resources_details.json','r',encoding='utf-8') as json_file:
                        coolresourcedata = json.load(json_file)
    if len(lang_support) != 0:
        print("inlang",l1)
        language = l1
    if len(subj) != 0:
        subject = s1
    if len(rsrc) != 0:
        rsrc_type = r1
    if len(grade) != 0:
        level = g1
    return render(request,"ndf/Thecooloer.html",{
                                    'title':'COOL-OER','coolresourcedata':coolresourcedata,'groupid':'home','group_id':'home','bannerpics':banner_pics1,'k_oers':koers,'koers_count':len(koers),'c_oers':coers,'coers_count':len(coers),'t_oers':toers,'toers_count':len(toers),'lang':language,'subjt':subject,'grade':level,'rsrc':rsrc_type
})

def cool_oer_preview(request,node_id):
    print("in cool oer preview")
    index = 'nodes'
    doc_type = 'node'
    q = Q('bool',must = [Q('match_phrase',name = node_id)])                                                    
    s1 = Search(using=es, index='nodes',doc_type="node").query(q)
    s2 = s1.execute()
    nd = s2[0]
    #print(nd.attribute_set)
    banner_pics1 = ['/static/ndf/OER_1200_300_Slider_1.jpg','/static/ndf/OER_1200_300_Slider_2.jpg','/static/ndf/OER_1200_300_Slider_3.jpg','/static/ndf/OER_1200_300_Slider_4.jpg','/static/ndf/OER_1200_300_Slider_5.jpg','/static/ndf/COOL_website_Banner_Banner_1200-300.png']
    
    with open('/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/ndf/static/ndf/cool_resources_details.json','r',encoding='utf-8') as json_file:
                        coolresourcedata = json.load(json_file)
    if 'sessionid' in request.COOKIES.keys():
        results = hit_counter.objects.filter(session_id=request.COOKIES['sessionid']).filter(visitednode_name=nd.name)
        if len(results) ==0:
            obj = hit_counter.objects.create(session_id=request.COOKIES['sessionid'],visitednode_id=nd.id,visitednode_name=nd.name,preview_count=1,visit_count=0,download_count=0,created_date=datetime.now(),last_updated=datetime.now())
            obj.save()
            print("hit_counter object saved")
        else:
            obj1 = results[0]
            #print "else:",obj1.visitednode_name,obj1.visit_count                                                                                                      
            if obj1.preview_count == 0:
                obj1.preview_count = 1
                obj1.save()
    #request.LANGUAGE_CODE = lang
    eng_nd = ''
    if 'en' in nd.language:
        q = Q('bool',must = [Q('match',subject = nd.id),Q('match',type= 'GRelation'),Q('match', relation_type= '5752ad572e01310a05dca50f')])
        sa1 = Search(using=es, index='triples',doc_type="triple").query(q)
        res1 = sa1.execute()
    else:
        q = Q('bool',must = [Q('match',type= 'GRelation'),Q('match', relation_type= '5752ad572e01310a05dca50f')])
        sa2 = Search(using=es, index='triples',doc_type="triple").query(q)
        res1 = sa2.execute()
        for each in sa2[0:sa2.count()]:
            if each.right_subject == nd.id:
                eng_nd = each.subject
        q = Q('bool',must = [Q('match',subject = eng_nd),Q('match',type= 'GRelation'),Q('match', relation_type= '5752ad572e01310a05dca50f')])
        sa1 = Search(using=es, index='triples',doc_type="triple").query(q)
        res2 = sa1.execute()
    nds = {}
    #print sa1.count()
    for each in sa1[0:sa1.count()]:
        print(each)
        trns_nd = get_node_by_id(each.right_subject)
        nds[trns_nd.language[0]] = trns_nd.name
        #trns_nd = ''
    if eng_nd:
        nds['en'] = eng_nd
    else:
        nds['en'] = node_id
    print(nds)

    from django.utils.translation import activate
    activate(nd.language[0])
    return render(request,"ndf/cool_preview.html",{'title':'COOL-OER','coolresourcedata':coolresourcedata,'groupid':'home','group_id':'home','bannerpics':banner_pics1,'nd':nd,'transnds':nds})

def cool_incr_explorecnt(request):
    #print "in cool oer explr incr cnt"
    #index = 'nodes'
    #doc_type = 'node'
    from django.shortcuts import redirect
    node_id = request.POST.get('node_id')
    link = request.POST.get('href_link')
    print("link:",link)
    nd = get_node_by_id(node_id)
    if 'sessionid' in request.COOKIES.keys():
        results = hit_counter.objects.filter(session_id=request.COOKIES['sessionid']).filter(visitednode_name=nd.name)
        if len(results) ==0:
            obj = hit_counter.objects.create(session_id=request.COOKIES['sessionid'],visitednode_id=nd.id,visitednode_name=nd.name,preview_count=0,visit_count=1,download_count=0,created_date=datetime.now(),last_updated=datetime.now())
            obj.save()
            print("hit_counter object saved")
        else:
            obj1 = results[0]
            #print "else:",obj1.visitednode_name,obj1.visit_count                                                                                                      
            if obj1.visit_count == 0:
                obj1.visit_count = 1
                obj1.save()
    print ("redirecting to link:",link)
    return redirect(link)

def site_contact(request,group_id):
    banner_pics = ['/static/ndf/Website Banners/About/about_2_mod.png','/static/ndf/Website Banners/About/About2.png','/static/ndf/Website Banners/About/About3.png','/static/ndf/Website Banners/About/About4.png']
    return render(request,"ndf/contact.html",{'title':'Contact','group_id': 'home', 'groupid': 'home','bannerpics':banner_pics})

def site_termsofuse(request,group_id):
    banner_pics = ['/static/ndf/Website Banners/About/about_2_mod.png','/static/ndf/Website Banners/About/About2.png','/static/ndf/Website Banners/About/About3.png','/static/ndf/Website Banners/About/About4.png']
    return render(request,"ndf/termsofservice.html",
                                        {
                                            'title': 'Terms Of Use','group_id': 'home', 'groupid': 'home','bannerpics':banner_pics,
                                        })

def site_credits(request,group_id):
    banner_pics = ['/static/ndf/Website Banners/About/about_2_mod.png','/static/ndf/Website Banners/About/About2.png','/static/ndf/Website Banners/About/About3.png','/static/ndf/Website Banners/About/About4.png']
    return render(request,"ndf/credits.html",{'title': 'Credits','group_id': 'home', 'groupid': 'home','bannerpics':banner_pics})

def site_privacypolicy(request,group_id):
    banner_pics = ['/static/ndf/Website Banners/About/about_2_mod.png','/static/ndf/Website Banners/About/About2.png','/static/ndf/Website Banners/About/About3.png','/static/ndf/Website Banners/About/About4.png']
    return render(request,"ndf/privacypolicy.html",{'title': 'Privacy Policy','group_id': 'home', 'groupid': 'home','bannerpics':banner_pics,
                                        })


def create_lang_module(request,group_id, module_id=None, cancel_url='e-library'):
    
    if request.method == "GET":
        template = 'ndf/cmspage.html'
        additional_form_fields = {}
        module_attrs = ['educationalsubject', 'educationallevel', 'languages', 'node_type']
        # ma: module attr
        module_attr_values = {ma: '' for ma in module_attrs}

        if module_id:
            # existing module.
            url_name = 'node_edit'
            url_kwargs={'group_id': group_id, 'node_id': module_id, 'detail_url_name': 'e-library'}
            # updating module attr dict:
            module_obj = Node.get_node_by_id(module_id)
            module_attr_values = module_obj.get_attributes_from_names_list(module_attrs)

        else:
            # new module
            url_name = 'node_create'
            url_kwargs={'group_id': group_id, 'member_of': 'Module', 'detail_url_name': 'e-library'}

    additional_form_fields = {
            'attribute': {
                'Subject': {
                    'name' :'educationalsubject',
                    'widget': 'dropdown',
                    'value': module_attr_values['educationalsubject'],
                    'all_options': GSTUDIO_RESOURCES_EDUCATIONAL_SUBJECT
                },
                'Grade': {
                    'name' :'educationallevel',
                    'widget': 'dropdown',
                    'widget_attr': 'multiple',
                    'value': module_attr_values['educationallevel'],
                    'all_options': GSTUDIO_RESOURCES_EDUCATIONAL_LEVEL
                },
                'languages': {
                    'name' :'language',
                    'widget': 'dropdown',
                    'widget_attr': 'multiple',
                    'value': module_attr_values['languages'],
                    'all_options': GSTUDIO_RESOURCES_LANGUAGES
                },
            }
        }

    return render(request,template,{
                                    'title': 'Module', 'node_obj': Node.get_node_by_id(module_id),
                                    'group_id': group_id, 'groupid': group_id,
                                    'additional_form_fields': additional_form_fields,
                                    'post_url': reverse(url_name, kwargs=url_kwargs)
                                } )
    
    '''print "Entered create_lang"
    template = 'ndf/cmspage.html'
    return render_to_response(template,{'group_id':group_id })
    '''

def create_lang_unit(request,group_id, unit_id=None, cancel_url='e-library'):

    if request.method == "GET":
        template = 'ndf/cmspagec.html'
        additional_form_fields = {}
        unit_attrs = ['languages']
        # ma: module attr                                                                                                                                              
        unit_attr_values = {ma: '' for ma in unit_attrs}

        if unit_id:
            # existing module.                                                                                                                                         
            url_name = 'node_edit'
            url_kwargs={'group_id': group_id, 'node_id': unit_id, 'detail_url_name': 'e-library'}
            # updating module attr dict:                                                                                                                               
            unit_obj = Node.get_node_by_id(unit_id)
            unit_attr_values = unit_obj.get_attributes_from_names_list(unit_attrs)

        else:
            # new module                                                                                                                                               
            url_name = 'node_create'
            url_kwargs={'group_id': group_id, 'member_of': 'announced_unit', 'detail_url_name': 'e-library'}
    
    additional_form_fields = {
          'attribute':{
                'languages': {
                    'name' :'language',
                    'widget': 'dropdown',
                    'widget_attr': 'multiple',
                    'value': unit_attr_values['languages'],
                    'all_options': GSTUDIO_RESOURCES_LANGUAGES
                },
            }
        }
    
    print("additional form fields",additional_form_fields)
    return render(request,template,{
                                    'title': 'Unit', 'node_obj': get_node_by_id(unit_id),
                                    'group_id': group_id, 'groupid': group_id,
                                    'additional_form_fields': additional_form_fields,
                                    'post_url': reverse(url_name, kwargs=url_kwargs)
                                } )


def node_create_edit(request,
                    group_id=None,
                    member_of=None,
                    detail_url_name=None,
                    node_type='GSystem',
                    node_id=None):
    '''
    creation as well as edit of node
    '''
    print("inside node_create_edit")
    # check for POST method to node update operation
    if request.method == "POST":
        '''
        # put validations
        if node_type not in node_collection.db.connection._registered_documents.keys():
            raise ValueError('Improper node_type passed')
        '''
        #print "inside post method",request.POST
        
        kwargs={}
        group_name, group_id = get_group_name_id(group_id)
        member_of_name, member_of_id = get_gst_name_id(member_of)
        
        if member_of == 'Module': # existing node object
            if request.POST.get('attribute_educationalsubject') == 'English':
                domain_name,domain_id = get_group_name_id('English')
            elif request.POST.get('attribute_educationalsubject') == 'Mathematics':
                domain_name,domain_id = get_group_name_id('Mathematics')
            else:
                domain_name,domain_id = get_group_name_id('Science')
            kwargs={
                    'group_set': [group_id,domain_id],
                    'member_of': member_of_id,
                    'created_by':1
                    }
            node_obj = eval('node_type()')

        else: # create new
            module_id = request.POST.get('module')
            print("module_id:",module_id)
            kwargs={
                    'group_set': [group_id,module_id],
                    'member_of': member_of_id,
                    'created_by':1
                    }
            node_obj = eval('node_type()')

        language = get_language_tuple(request.POST.get('attribute_language', None))
        
        node_obj.fill_gstystem_values(request=request,
                                    language=language,
                                            **kwargs)
        print("bfr saving",node_obj)
        node_obj.save(group_id=group_id)
        print("node created:",node_obj)

        #document = node_obj.to_json_type()
        doc = json.dumps(node_obj, cls=NodeJSONEncoder)
        document = json.loads(doc)
        print("json document:",document)
        
        with open("/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/gstudio_configs/req_body.json",'r',encoding='utf-8') as req_body:
            request_body = json.load(req_body)
            print("request json",request_body)

        if document.get("_id"):
            document["id"] = document.pop("_id")
            document["type"] = document.pop("_cls")

            print("before indexing")
            es.index(index='nodes', doc_type='node', id=document["id"], body=document)
            if member_of == 'Module':
                print("domain_id",domain_id)
                q = Q('match',id = str(domain_id))
                s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.collection_set.add(params.val)", lang="painless",params={'val':document["id"]})
                s2 = s1.execute()
            else:
                q = Q('match',id = str(module_id))
                s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.collection_set.add(params.val)", lang="painless",params={'val':document["id"]})
                s2 = s1.execute()
        return HttpResponseRedirect(reverse(detail_url_name, kwargs={'group_id': group_id}))


def node_name_content_edit(request,group_id,node_id):
    print("inside node_name_content_edit")
    if request.method == "GET":
        req_context = {
                                    'title': 'Node Edit', 'node_obj': get_node_by_id(node_id),
                                    'group_id': group_id, 'groupid': group_id, 'node_id':node_id
                                }

    if request.method == "POST":
        #node_obj = get_node_by_id(node_id)
        name = request.POST.get('name')
        altnames = request.POST.get('altnames')
        content = request.POST.get('content')
        tags = request.POST.get('tags')
        print("updated_values:",str(name).encode('utf-8'),str(content).encode('utf-8'),str(altnames).encode('utf-8'))
        
        q = Q('bool',must = [Q('match',id = node_id)])
        #f1 = "relation_set." + "translation_of"
        s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.name = params.val1;ctx._source.altnames = params.val2;ctx._source.content = params.val3;ctx._source.tags.add(params.val4)", lang="painless",params={'val1':name, 'val2':altnames, 'val3': content, 'val4': tags})
        s2 = s1.execute()
        req_context = {
                                    'title': 'Node Edit', 'node_obj': get_node_by_id(node_id),
                                    'group_id': group_id, 'groupid': group_id, 'node_id':node_id
                                }
    template = 'ndf/node_edit.html'
    return render(request,template, req_context)
        

def fetch_modules_of_language(request,group_id):
    member_of_name, member_of_id = get_gst_name_id('Module')
    lang = request.POST.get("language")
    print("inside fetch modules of particular language:",lang)
    domain_set = ['English','Mathematics','Science']
    domain_nds = [get_group_name_id(each)[1] for each in domain_set]
    domains = get_nodes_by_ids_list(domain_nds)
    moduleids = []
    for each in domains:
        moduleids.extend(each.collection_set)
    print("moduleids:",moduleids)
    q= Q('bool', must=[Q('match', member_of = str(member_of_id)), Q('match',status='PUBLISHED'),Q('terms',id = moduleids),Q('match_phrase',language = lang)])
    s1 = (Search(using=es,index = 'nodes',doc_type='node').query(q)).sort({"last_update" : {"order" : "asc"}})
    s2 = s1.execute()

    modules = {}
    for each in s1[0:s1.count()]:
        modules[each.name] = each.id
    print("Modules:",json.dumps(modules))
    return HttpResponse(json.dumps(modules), content_type="application/json")

def coolpage(request):
    print("Entered coolpage")
    #TheCOOL.html
    q = Q('match', name = 'home')
    s1 = Search(using=es, index='nodes',doc_type="node").query(q)
    s2 = s1.execute()
    banner_pics1 = ['/static/ndf/OER_1200_300_Slider_1.jpg','/static/ndf/OER_1200_300_Slider_2.jpg','/static/ndf/OER_1200_300_Slider_3.jpg','/static/ndf/OER_1200_300_Slider_4.jpg','/static/ndf/OER_1200_300_Slider_5.jpg','/static/ndf/COOL_website_Banner_Banner_1200-300.png']
    if 'sessionid' in request.COOKIES.keys():
        results = hit_counter.objects.filter(session_id=request.COOKIES['sessionid']).filter(visitednode_name='TISS-COOL')
        if len(results) ==0:
            obj = hit_counter.objects.create(session_id=request.COOKIES['sessionid'],visitednode_id = s2[0].id,visitednode_name='TISS-COOL',preview_count=0,visit_count=1,download_count=0,created_date=datetime.now(),last_updated=datetime.now())
            obj.save()
            print("hit_counter object saved")
        else:
            obj1 = results[0]
            #print "else:",obj1.visitednode_name,obj1.visit_count                                                                                                      
            if obj1.visit_count == 0:
                obj1.visit_count = 1
                obj1.save()
            else:
                obj1.visit_count += 1
                obj1.save()
    req_context = {'title':'COOL','group_id': 'home', 'groupid': 'home','bannerpics':banner_pics1}
    return render(request,"ndf/TheCOOL.html",req_context)

def homepage(request, group_id):
    print("Entered home.py")
    #print request,"\n"                                                                                                                                                
    print(request.META,request.GET,request.POST,request.COOKIES,"\n")
    #print(request.author)
    if request.user.is_authenticated:
        print("user name:",request.user.id)
        q = eval("Q('bool', must=[Q('match', type = 'Author'), Q('match',created_by=int(request.user.id))])")
        # q = Q('match',name=dict(query='File',type='phrase'))                                                                                                         
        auth1 = Search(using=es, index=index,doc_type="node").query(q)
        auth2 = auth1.execute()
        print("auth1:",auth2[0].name)
        auth = auth2[0]
        # This will create user document in Author collection to behave user as a group.                                                                               
        print(GSTUDIO_SITE_LANDING_PAGE, request.user.id)
        if GSTUDIO_SITE_LANDING_PAGE == "home":
            print("before reverse")
            return HttpResponseRedirect( reverse('e-library'), kwargs={"groupid": group_id} )
        else:
            return HttpResponseRedirect( reverse('dashboard', kwargs={"group_id": request.user.id}) )
    else:
        print("in home:",group_id,GSTUDIO_SITE_LANDING_PAGE)
        if GSTUDIO_SITE_LANDING_PAGE == "home":
            print(request)
            #return HttpResponse("This is test",content_type='text/plain')
            return HttpResponseRedirect(  reverse('e-library', kwargs={"groupid": group_id} ) )
        else:
            return HttpResponseRedirect( reverse('groupchange', kwargs={"group_id": group_id}) )

def help(request,group_id):
    banner_pics = ['/static/ndf/Website Banners/Landing Page/elibrary1.png','/static/ndf/Website Banners/Landing Page/elibrary2.png','/static/ndf/elibrary 6.1.png','/static/ndf/Website Banners/Landing Page/elibrary4.png','/static/ndf/Website Banners/Landing Page/elibrary5.png','/static/ndf/Website Banners/Landing Page/elibrary6.png']
    template = 'ndf/help.html'
    return render(request,template, {'groupid':'home','group_id':group_id,'bannerpics':banner_pics})

def help_videos(request,group_id):
    node_id = request.POST.get('node_id')
    nd = get_node_by_id(node_id)
    if nd.language[0] != 'en':
        rel_set = nd.relation_set
        for each in rel_set:
            if 'translation_of' in each:
                engnd_id = each['translation_of']
                engnd = get_node_by_id(engnd_id)
                chkname = engnd.name
                print("chkname:",chkname)
    else:
        #nd = get_node_by_id(node_id)
        chkname = nd.name

    print('inside help_videos',node_id)
    with open('/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/ndf/static/ndf/module.json','r') as fd:
        json_data = json.load(fd)
    videos = json_data[str(chkname)]
    print("videos:",videos)
    template = 'ndf/thehelpmodal.html'
    return render(request,template, {'group_id':group_id , 'videos':videos , 'module_name':nd.name })
    
def explore_item(request,group_id):
    from django.shortcuts import redirect
    node_id = request.POST.get('node_id')
    link = request.POST.get('href_link')
    print("inside explore link",node_id,link)
    nd = get_node_by_id(node_id)
    if 'sessionid' in request.COOKIES.keys():
        results = hit_counter.objects.filter(session_id=request.COOKIES['sessionid']).filter(visitednode_name=nd.name)
        if len(results) ==0:
            obj = hit_counter.objects.create(session_id=request.COOKIES['sessionid'],visitednode_id=nd.id,visitednode_name=nd.name,preview_count=0,visit_count=1,download_count=0,created_date=datetime.now(),last_updated=datetime.now())
            obj.save()
            print("hit_counter object saved")
        else:
            obj1 = results[0]
            print("else:",obj1.visitednode_name,obj1.visit_count)
            if obj1.visit_count == 0:
                obj1.visit_count = 1
                obj1.save()
    return redirect(link)

def get_file(md5_or_relurl=None):
    file_blob = None
    try:
        if md5_or_relurl:
            file_blob = gfs.open(md5_or_relurl)
    except Exception as e:
        print("File '", md5_or_relurl, "' not found: ", e)
    return file_blob

def readDoc(request, group_id,file_id):
    '''Return Files
    '''
    try:
        group_id = ObjectId(group_id)
    except:
        group_name, group_id = get_group_name_id(group_id)

    print("in readDoc")
    file_node = get_node_by_id(file_id)
    groupnd = get_node_by_id(group_id)
    print("Session:",request.COOKIES['sessionid'])
    #print("tags:",file_node.tags)
    if file_node.tags[0].find('unplatform')>=0:
        results = hit_counter.objects.filter(session_id=request.COOKIES['sessionid']).filter(visitednode_name=groupnd.name)
    else:
        results = hit_counter.objects.filter(session_id=request.COOKIES['sessionid']).filter(visitednode_name=file_node.name)
    if len(results) ==0:
        if file_node.tags[0].find('unplatform')>=0:
            obj = hit_counter.objects.create(session_id=request.COOKIES['sessionid'],visitednode_id=file_node.id,visitednode_name=groupnd.name,preview_count=0,visit_count=0,download_count=1,created_date=datetime.now(),last_updated=datetime.now())
            print("post if creation of unplatfom")
        else:
            obj = hit_counter.objects.create(session_id=request.COOKIES['sessionid'],visitednode_id=file_node.id,visitednode_name=file_node.name,preview_count=0,visit_count=0,download_count=1,created_date=datetime.now(),last_updated=datetime.now())
        obj.save()
        print("object saved successfully")
    else:                                                                                                                                                          
        #cnt = results[0].download_count                                                                                                                          
        obj1 = results[0]
        if obj1.download_count == 0:
            obj1.download_count = 1                                                                                                                                 
            obj1.save()
        if file_node.tags[0].find('handbook') >= 0:
            if obj1.visit_count == 0:
                obj1.visit_count = 1
                obj1.save()
            if obj1.download_count == 0:
                obj1.download_count = 1
                obj1.save()
        
    if file_node is not None:
        if file_node.if_file.original.relurl:
            if file_node.tags[0].find('unplatform')>=0:
                from django.http import StreamingHttpResponse
                from wsgiref.util import FileWrapper
                chunk_size = 8192
                #response['X-Accel-Redirect']='/downloadables/%s'%(file_node.if_file.original.relurl).split('/')[-1] 
                print(file_node.name)
                filename = file_node.name+'.exe'
                file_path = '/data/media/'+file_node.if_file.original.relurl
                response = StreamingHttpResponse(
                    FileWrapper(open(file_path, 'rb'), chunk_size),
                    content_type="application/octet-stream"
                )
                response['X-Accel-Redirect']='/media/%s'%(file_node.if_file.original.relurl) 
                response['Content-Length'] = os.path.getsize(file_path)    
                response['Content-Disposition'] = "attachment; filename=%s" % filename
                return response
            else:
                print("in unplatform else")
                return HttpResponse(get_file(file_node.if_file.original.relurl),content_type=file_node.if_file.mime_type)
    else:
        return HttpResponse("")


def about(request,group_id):
    banner_pics = ['/static/ndf/Website Banners/About/about_2_mod.png','/static/ndf/Website Banners/About/About2.png','/static/ndf/Website Banners/About/About3.png','/static/ndf/Website Banners/About/About4.png']
    template = 'ndf/about.html'
    return render(request,template, {'groupid':'home','group_id':group_id , 'bannerpics':banner_pics})


def send_message(request,group_id):
    #template = 'ndf/about.html'
    #return render_to_response(template, {'group_id':group_id})
    from django.core.mail import send_mail, EmailMultiAlternatives
    from django.contrib import messages
    print("send message",EMAIL_HOST_USER)
    print(request,request.POST)
    #subject = 'Feedback message'
    domain = request.POST.get('domain','')
    if domain == '':
        domain = 'About'
    subject = 'Feedback message from '+domain
    message = 'feedback received for'+domain
    c = {'email': request.POST['email'],
                 'first_name': request.POST['first_name'],'last_name':request.POST['last_name'],'domain':request.POST['domain'],'message':request.POST['message']}
    email_from = EMAIL_HOST_USER
    recipient_list = ['contact@clix.tiss.edu']
    html_content = render_to_string('ndf/html_message.html', c)
    msg = EmailMultiAlternatives(subject, message,email_from, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=True)
    messages.success(request, 'Your feedback sent successfully!')
    if domain == 'cool':
        return HttpResponseRedirect( reverse('coolpage') )
    elif domain != 'About':
        return HttpResponseRedirect( reverse('domain_page', kwargs={"group_id": group_id,"domain_name":request.POST['domain']}) )
    else:
        return HttpResponseRedirect( reverse('about', kwargs={"group_id": group_id}) )


def domain_help(request,group_id,domain_name):
    print("inside domain help",domain_name)
    if domain_name == 'English':
        template = 'ndf/theEDhelp.html'
        banner_pics = ['/static/ndf/Website Banners/English Domain/eng dnd.png','/static/ndf/Website Banners/English Domain/English2.png','/static/ndf/Website Banners\English Domain/English1.png']

    if domain_name == 'Mathematics':
        template = 'ndf/theMDhelp.html'
        banner_pics = ['/static/ndf/Website Banners/Maths Domain/math dnd.png','/static/ndf/Website Banners/Maths Domain/math1.png','/static/ndf/Website Banners/Maths Domain/math2.png']
    if domain_name == 'Science':
        template = 'ndf/theSDhelp.html'
        banner_pics = ['/static/ndf/Website Banners/Science Domain/sci dnd.png','/static/ndf/Website Banners/Science Domain/science1.png','/static/ndf/Website Banners/Science Domain/science2.png']
    return render(request,template, {'bannerpics':banner_pics,'groupid':'home','group_id':group_id,'domain_name':domain_name})


def loadDesignDevelopment(request,group_id,domain_name):
    print("inside Design Development:",domain_name)
    if domain_name == 'English':
        if request.LANGUAGE_CODE == 'en':
            template = 'ndf/ED.html'
        elif request.LANGUAGE_CODE == 'hi':
            template = 'ndf/theEDHindi.html'
        else:
            template = 'ndf/theEDTelgu.html'
        banner_pics = ['/static/ndf/Website Banners/English Domain/eng dnd.png','/static/ndf/Website Banners/English Domain/English2.png','/static/ndf/Website Banners\English Domain/English1.png']
       
    if domain_name == 'Mathematics':
        if request.LANGUAGE_CODE == 'en':
            template = 'ndf/MD.html'
        elif request.LANGUAGE_CODE == 'hi':
            template = 'ndf/theMDHindi.html'
        else:
            template = 'ndf/theMDTelgu.html'
        banner_pics = ['/static/ndf/Website Banners/Maths Domain/math dnd.png','/static/ndf/Website Banners/Maths Domain/math1.png','/static/ndf/Website Banners/Maths Domain/math2.png']
    if domain_name == 'Science':
        if request.LANGUAGE_CODE == 'en':
            template = 'ndf/SD.html'
        elif request.LANGUAGE_CODE == 'hi':
            template = 'ndf/theSDhindi.html'
        else:
            template = 'ndf/theSDTelgu.html'
        banner_pics = ['/static/ndf/Website Banners/Science Domain/sci dnd.png','/static/ndf/Website Banners/Science Domain/science1.png','/static/ndf/Website Banners/Science Domain/science2.png']
    return render(request,template, {'bannerpics':banner_pics,'groupid':'home','group_id':group_id,'domain_name':domain_name})


def uploadDoc(request, group_id):
    print("inside")
    group_name, group_id = get_group_name_id(group_id)
    print("inside upload doc",group_name,group_id)
    if request.method == "GET":
        template = "ndf/Upload_docu.html"
    variable = {'groupid':group_id,'group_id':group_id}
    return render(request,template, variable)


def upload_using_save_file(request,group_id):
    from gnowsys_ndf.ndf.views.file import save_file
    try:
        group_id = ObjectId(group_id)
    except:
        group_name, group_id = get_group_name_id(group_id)

    group_obj = node_collection.find_one({'_id': ObjectId(group_id)})
    title = request.POST.get('context_name','')
    sel_topic = request.POST.get('topic_list','')
    
    usrid = 1
    name  = request.POST.get('name')
    
    #from gnowsys_ndf.ndf.views.filehive import write_files
    #is_user_gstaff = check_is_gstaff(group_obj._id, request.user)
    content_org = request.POST.get('content_org', '')
    uploaded_files = request.FILES.getlist('filehive', [])
    # gs_obj_list = write_files(request, group_id)
    # fileobj_list = write_files(request, group_id)
    # fileobj_id = fileobj_list[0]['_id']
    fileobj_list = write_files(request, group_id,unique_gs_per_file=False)
    # fileobj_list = write_files(request, group_id)
    fileobj_id = fileobj_list[0]['_id']
    file_node = node_collection.find_one({'_id': ObjectId(fileobj_id) })

    #discussion_enable_at = node_collection.one({"_type": "AttributeType", "name": "discussion_enable"})
    for each_gs_file in fileobj_list:
        #set interaction-settings
        each_gs_file.status = u"PUBLISHED"
        if usrid not in each_gs_file.contributors:
            each_gs_file.contributors.append(usrid)

        group_object = node_collection.find_one({'_id': ObjectId(group_id)})
        
        each_gs_file.save()
        save_node_to_es(each_gs_file)
        #create_gattribute(each_gs_file._id, discussion_enable_at, True)
        #return_status = create_thread_for_node(request,group_obj._id, each_gs_file)

    return HttpResponseRedirect( reverse('e-library', kwargs={"group_id": group_id}))
    # return HttpResponseRedirect(url_name)

def write_files(request, group_id, make_collection=False, unique_gs_per_file=True, **kwargs):
    print("in write files")
    group_name, group_id = get_group_name_id(str(group_id))
    user_id = 1

    # author_obj = node_collection.one({'_type': u'Author', 'created_by': int(user_id)})
    author_obj = Author.get_author_obj_from_name_or_id(user_id)
    author_obj_id = author_obj._id
    kwargs['created_by'] = user_id

    first_obj      = None
    collection_set = []
    uploaded_files = request.FILES.getlist('filehive', [])
    name           = request.POST.get('name')
    print("files:",request.FILES.getlist('filehive', []))
    gs_obj_list    = []
    for each_file in uploaded_files:
        gs_obj = GSystem()
        language = request.POST.get('language')
        language = get_language_tuple(language)
        group_set = [ObjectId(group_id),ObjectId(author_obj_id)]

        if name and not first_obj and (name != 'untitled'):
            file_name = name
        else:
            file_name = each_file.name if hasattr(each_file, 'name') else name

        existing_file_gs = gs_obj.fill_gstystem_values(request=request,
                                    name=file_name,
                                    group_set=group_set,
                                    language=language,
                                    uploaded_file=each_file,
                                    unique_gs_per_file=unique_gs_per_file,
                                    **kwargs)
        print("existing_file_gs",existing_file_gs)
        q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='File')])")
        GST_FILE = (Search(using=es,index = 'nodes',doc_type='node').query(q)).execute()
        gst_file_id = GST_FILE[0].id
        if (gs_obj.get('_id', None) or existing_file_gs.get('_id', None)) and \
           (existing_file_gs.get('_id', None) == gs_obj.get('_id', None)):
            if gst_file_id not in gs_obj.member_of:
                gs_obj.member_of.append(ObjectId(gst_file_id))

            gs_obj.save(groupid=ObjectId(group_id),validate=False)
            save_node_to_es(gs_obj)
            if 'video' in gs_obj.if_file.mime_type:
                convertVideo.delay(user_id, str(gs_obj._id), file_name)
            if not first_obj:
                first_obj = gs_obj
            else:
                collection_set.append(gs_obj._id)

            gs_obj_list.append(gs_obj)
        elif existing_file_gs:
                gs_obj_list.append(existing_file_gs)

    if make_collection and collection_set:
        first_obj.collection_set = collection_set
        print("first_obj:",first_obj)
        first_obj.save()
        save_node_to_es(first_obj)
    return gs_obj_list

    # return render_to_response('ndf/filehive.html', {
    #   'group_id': group_id, 'groupid': group_id,
    #   }, context_instance=RequestContext(request))


def domain_page(request,group_id,domain_name):
    import json
    print("es_queries domain page:",domain_name,request.session.session_key)
    domain_id = get_name_id_from_type(domain_name,'Group')[1]
    #print "domain id:",domain_id
    domainnd = get_node_by_id(domain_id)
    #print "domain nd:",domainnd
    lang = request.LANGUAGE_CODE
    files = get_nodes_by_ids_list(list(domainnd.collection_set))
    finalfiles = []

    if domainnd.name =='Mathematics' or domainnd.name == 'Science':
        for each in files:
            if each.language[0] == lang:
                finalfiles.append(each)
        files = sorted(finalfiles, key=lambda nd: nd.last_update)
    else:
        files = sorted(files, key=lambda nd: nd.last_update)
    #print request.META["CSRF_COOKIE"]
    #CSRF_COOKIE = request.META["CSRF_COOKIE"]

    if domainnd.name == 'English':
        banner_pics = ['/static/ndf/Website Banners/English Domain/eng dnd.png','/static/ndf/Website Banners/English Domain/English2.png','/static/ndf/Website Banners/English Domain/English1.png']
    elif domainnd.name == 'Mathematics':
        banner_pics = ['/static/ndf/Website Banners/Maths Domain/math dnd.png','/static/ndf/Website Banners/Maths Domain/math1.png','/static/ndf/Website Banners/Maths Domain/math2.png']
    else:
        banner_pics = ['/static/ndf/Website Banners/Science Domain/sci dnd.png','/static/ndf/Website Banners/Science Domain/science1.png','/static/ndf/Website Banners/Science Domain/science2.png']

    import os
    #print "re",files,os.getcwd()
    with open('/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/ndf/static/ndf/employees.json','r',encoding='utf-8') as json_file:
        employeedata = json.load(json_file)
    with open('/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/ndf/static/ndf/testimonial.json','r',encoding='utf-8') as json_file:
        testimonydata = json.load(json_file)
    print("COOKIES:",request.COOKIES)
    results = hit_counter.objects.filter(session_id=request.COOKIES['sessionid'],visitednode_name=domainnd.name)
    if len(results) ==0:
        obj = hit_counter.objects.create(session_id=request.COOKIES['sessionid'],visitednode_id=domainnd.id,visitednode_name=domainnd.name,preview_count=0,visit_count=1,download_count=0,created_date=datetime.now(),last_updated=datetime.now())
        obj.save()
    return render(request,
            "ndf/domain.html",
            {"employee":employeedata,"testimony":testimonydata,"files":files,"first_arg":domain_name,'groupid':'home',"group_id":group_id,"bannerpics":banner_pics}) 
    
def get_module_previewdata(request,group_id):

    '''
    ARGS: module_obj
    Result will be of following form:
    {
        name: 'Module1',
        grade : [],
        subject : science,
        unit_details: [
            {
                name: 'Unit 1',
                lessn: 'Lessn 1',
                activities: 10
            },
            {
                name: 'Unit 1',
                type: 'Lessn 2',
                activities: 10
            }
        ]
    }
    '''
    node_id = request.POST.get("node_id")

    print("in es-queries: get_module_previewdata",node_id,request.session.session_key)
    node_obj = get_node_by_id(node_id)


    units = get_attribute_value(node_id,'items_sort_list')
    #print("unitnds:",units)
    if units == 'None' or len(units) == 0:
        units = get_nodes_by_ids_list(node_obj.collection_set)
    else:
        units = list(units)
    #print("units:",units)
    #imgsrc = get_attribute_value(node_id,'has_banner_pic')
    # unitnds = get_nodes_by_ids_list(list(node_obj.collection_set))
    module_dict = {}

    module_dict['name'] = node_obj.altnames
    module_dict['grade'] = get_attribute_value(node_id,'educationallevel')
    module_dict['subject'] = get_attribute_value(node_id,'educationalsubject')
    module_dict['image'] = get_relation_value(node_id,'has_banner_pic')
    module_dict['content'] = node_obj.content
    module_dict['unitdetails'] = []
    module_dict['id'] = node_obj.id
    module_dict['grade'] = [str(each) for each in module_dict['grade']]
    module_dict['language'] = node_obj.language
    if node_obj.language[0] != 'en':
        rel_set = node_obj.relation_set
        for each in rel_set:
            if 'translation_of' in each:
                engnd_id = each['translation_of']
                engnd = get_node_by_id(engnd_id)
                chkname = engnd.name
                print("chkname:",chkname)
    else:
        chkname = module_dict['name']


    q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='File')])")
    GST_FILE = (Search(using=es,index = 'nodes',doc_type='node').query(q)).execute()
    
    q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='Page')])")
    GST_PAGE = (Search(using=es,index = 'nodes',doc_type='node').query(q)).execute()
    
    q= eval("Q('bool', must=[Q('match', type = 'GSystemType'), Q('match',name='Jsmol')])")
    GST_JSMOL = (Search(using=es,index = 'nodes',doc_type='node').query(q)).execute()

    if node_obj.language[0] != 'en':
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',language = node_obj.language[1]),Q('match_phrase',tags = 'Handbook'),Q('match_phrase',tags = chkname.split()[0]),Q('match_phrase',tags = 'Student')])
    else:
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',language = node_obj.language[1]),Q('match_phrase',tags = 'Handbook'),Q('match_phrase',tags = module_dict['name'].split()[0]),Q('match_phrase',tags = 'Student')])

    alldocs1 = (Search(using=es,index = 'nodes',doc_type='node').query(q)).sort({"last_update" : {"order" : "desc"}})
    alldocs2 = alldocs1.execute()

    print("document count:",alldocs1.count())
    student_docs = {}
    if alldocs1.count() > 0 :
        for each in alldocs2:
            student_docs[str(each.language[1])]='/media/'+str(each.if_file.original.relurl)
    print("docs:",student_docs)
    
    if node_obj.language[0] != 'en':
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',language = node_obj.language[1]),Q('match_phrase',tags = 'Handbook'),Q('match_phrase',tags = chkname.split()[0]),Q('match_phrase',tags = 'Teacher')])
    else:
        q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',language = node_obj.language[1]),Q('match_phrase',tags = 'Handbook'),Q('match_phrase',tags = module_dict['name'].split()[0]),Q('match_phrase',tags = 'Teacher')])
    
    alldocs1 = (Search(using=es,index = 'nodes',doc_type='node').query(q)).sort({"last_update" : {"order" : "desc"}})
    alldocs2 = alldocs1.execute()
    
    teacher_docs = {}
    
    if alldocs1.count() > 0 :
        for each in alldocs2:
            teacher_docs[str(each.language[1])]='/media/'+str(each.if_file.original.relurl)
    print("docs:",teacher_docs)
    q1 = []
    for each in str(chkname).split():
        q1.append(Q('match_phrase', tags = each))
    #print node_obj.language[1]

    q = Q('bool',must=[Q('terms',member_of=[GST_FILE[0].id,GST_JSMOL[0].id,GST_PAGE[0].id]),Q('match',access_policy='PUBLIC'),Q('match_phrase',language = node_obj.language[1]),Q('match_phrase',tags = 'Tool')],should = q1,minimum_should_match=1)
                
    print("interactives query:",q)
    allinteractives1 = (Search(using=es,index = 'nodes',doc_type='node').query(q)).sort({"last_update" : {"order" : "desc"}})

    allinteractives2 = allinteractives1.execute()

    with open('/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/ndf/static/ndf/theInteractive.json','r') as json_file:
        tooldata = json.load(json_file)
    interactives_data ={}
    for each in allinteractives1:
        #print(each.name,each.tags,str(each.altnames).encode('utf-8'))
        interactives_data[str(each.altnames)] = [tooldata[str(each.name)]['Interactive_href'],tooldata[str(each.name)]['Interactive_image']]

    #print(q,allinteractives1.count(),interactives_data)

    for each in units:
        #print "collection_set:",each.collection_set,each.id
        lessnnds = get_nodes_by_ids_list(list(each.collection_set))
        lessnnds = sorted(lessnnds, key=lambda nd: nd.last_update)
        #print "lessnnds:",lessnnds
        for lessn in lessnnds:
            unitdict = {}
            unitdict['name'] = each.altnames
            # print "lessnnds:",each.collection_set
            #print("lessn name:",(lessn.name))
            unitdict['lessname'] = (lessn.name)
            unitdict['totalactivities'] = len(list(lessn.collection_set))
            module_dict['unitdetails'].append(unitdict) 
    #print("module details:",module_dict)
    
    with open('/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/ndf/static/ndf/employees.json','r',encoding='utf-8') as fd:
        json_data = json.load(fd)
    if module_dict['subject'] == 'English':
        authorData = json_data['Team_detail_english']
    elif module_dict['subject'] == 'Mathematics':
        authorData = json_data['Team_detail_math']
    elif module_dict['subject'] == 'Digital Literacy':
       # print json_data['Team_detail_digital']
        authorData = json_data['Team_detail_digital']
    else:
        authorData = json_data['Team_detail_science']
    #print "Author data of module:",authorData
    userdata = []
    leaduser = []
    
    for each in authorData:
        #engnd_id = node_obj.relation_set[0]['translation_of']
        #print engnd_id
        if each['moduleId'] == chkname:
            print("before assigninig user data")
            userdata = each['userIdArray']
            leaduser = each['u']
            break
    print("Author data of module:",userdata)
    
    results = hit_counter.objects.filter(session_id=request.COOKIES['sessionid']).filter(visitednode_name=module_dict['name'])
    if len(results) ==0:
        obj = hit_counter.objects.create(session_id=request.COOKIES['sessionid'],visitednode_id=module_dict['id'],visitednode_name=module_dict['name'],preview_count=1,visit_count=0,download_count=0,created_date=datetime.now(),last_updated=datetime.now())
        obj.save()
        print("hit_counter object saved")
    else:
        obj1 = results[0]
        #print "else:",obj1.visitednode_name,obj1.visit_count
        if obj1.preview_count == 0:
            obj1.preview_count = 1
            obj1.save()

    return render(request,'ndf/Emodule_preview.html',
            {
                'group_id': group_id, 'groupid': group_id,
                'moduledetails':module_dict, 'student_docs':student_docs,'teacher_docs':teacher_docs, 'interactivestotal':allinteractives1.count(), 'toolsdata':interactives_data, 'userdata':userdata, 'leaduser':leaduser
            })

def get_node_by_id(node_id):
    '''
        Takes ObjectId or objectId as string as arg
            and return object
    '''
    #print "node id:",node_id
    if node_id:
        q = eval("Q('match', id = str(node_id))")

        # q = Q('match',name=dict(query='File',type='phrase'))
        s1 = Search(using=es, index='nodes',doc_type="node").query(q)
        s2 = s1.execute()
        #print "get_node_by_id s2",s2,q
        return s2[0]

        # return node_collection.one({'_id': ObjectId(node_id)})
    else:
        # raise ValueError('No object found with id: ' + str(node_id))
        return None

def get_nodes_by_ids_list(node_id_list):
    '''
        Takes list of ObjectIds or objectIds as string as arg
            and return list of object
    '''
    # try:
    #     node_id_list = map(ObjectId, node_id_list)
    # except:
    #     node_id_list = [ObjectId(nid) for nid in node_id_list if nid]
    if node_id_list:
        node_id_list = [str(each) for each in node_id_list]
        q = eval("Q('terms', id = node_id_list)")
        print(q)
        # q = Q('match',name=dict(query='File',type='phrase'))
        s1 = Search(using=es, index='nodes',doc_type="node").query(q)
        s2 = s1.execute()
        return s1[0:s1.count()]
        # return node_collection.find({'_id': {'$in': node_id_list}})
    else:
        return None


def get_node_obj_from_id_or_obj(node_obj_or_id, expected_type):
    # confirming arg 'node_obj_or_id' is Object or oid and
    # setting node_obj accordingly.
    node_obj = None

    if node_obj_or_id.type == expected_type:
        node_obj = node_obj_or_id
    elif isinstance(node_obj_or_id,ObjectId):
        q = eval("Q('match', id = node_id)")

        # q = Q('match',name=dict(query='File',type='phrase'))
        s1 = Search(using=es, index='nodes',doc_type="node").query(q)
        s2 = s1.execute() 
        node_obj = s2[0]
    else:
        # error raised:
        raise RuntimeError('No Node class instance found with provided arg for get_node_obj_from_id_or_obj(' + str(node_obj_or_id) + ', expected_type=' + str(expected_type) + ')')

    return node_obj

def get_group_name_id(group_name_or_id, get_obj=False):
    '''
      - This method takes possible group name/id as an argument and returns (group-name and id) or group object.

      - If no second argument is passed, as method name suggests, returned result is "group_name" first and "group_id" second.

      - When we need the entire group object, just pass second argument as (boolian) True. In the case group object will be returned.

      Example 1: res_group_name, res_group_id = get_group_name_id(group_name_or_id)
      - "res_group_name" will contain name of the group.
      - "res_group_id" will contain _id/ObjectId of the group.

      Example 2: res_group_obj = get_group_name_id(group_name_or_id, get_obj=True)
      - "res_group_obj" will contain entire object.

      Optimization Tip: before calling this method, try to cast group_id to ObjectId as follows (or copy paste following snippet at start of function or wherever there is a need):
      try:
          group_id = ObjectId(group_id)
      except:
          group_name, group_id = get_group_name_id(group_id)

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
        q = eval("Q('match', id = str(group_name_or_id))")
        print("befr query:",q)
        # q = Q('match',name=dict(query='File',type='phrase'))
        s1 = Search(using=es, index='nodes',doc_type="node").query(q)
        s2 = s1.execute() 
        group_obj = s2[0]
        # group_obj = node_collection.one({"_id": ObjectId(group_name_or_id)})

        # checking if group_obj is valid
        if group_obj:
            # if (group_name_or_id == group_obj._id):
            group_id = group_name_or_id
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
        q = eval("Q('bool',must =[Q('match', name = group_name_or_id), Q('terms', type = ['Group', 'Author'])])")
        print("query:",q)
        # q = Q('match',name=dict(query='File',type='phrase'))
        s1 = Search(using=es, index='nodes',doc_type="node").query(q)
        s2 = s1.execute() 
        group_obj = s2[0]
        # group_obj = node_collection.one(
        #     {"_type": {"$in": ["Group", "Author"]}, "name": unicode(group_name_or_id)})

        # checking if group_obj is valid
        if group_obj:
            # if (group_name_or_id == group_obj.name):
            group_name = group_name_or_id
            group_id = group_obj.id

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

def get_group_type(group_id, user):
    """This function checks for url's authenticity
    
    """

    #print "in get_group_type function"
    try:
        # Splitting url-content based on backward-slashes
        split_content = group_id.strip().split("/")

        # Holds primary key, group's ObjectId or group's name
        g_id = ""
        if split_content[0] != "":
            g_id = split_content[0]
        else:
            g_id = split_content[1]

        group_node = None

        if g_id.isdigit() and 'dashboard' in group_id:
            # User Dashboard url found
            u_id = int(g_id)
            user_obj = User.objects.get(pk=u_id)

            if not user_obj.is_active:
                error_message = "\n Something went wrong: Either url is invalid or such group/user doesn't exists !!!\n"
                raise Http404(error_message)

        else:
            # Group's url found
            if ObjectId.is_valid(g_id):
                # Group's ObjectId found
                q = eval("Q('bool',must =[Q('match', id = ObjectId(g_id)), Q('terms', type = ['Group', 'Author'])])")

                # q = Q('match',name=dict(query='File',type='phrase'))
                s1 = Search(using=es, index='nodes',doc_type="node").query(q)
                s2 = s1.execute() 
                group_node = s2[0]
                
                # group_node = node_collection.one({'_type': {'$in': ["Group", "Author"]}, '_id': ObjectId(g_id)})

            else:
                # Group's name found

                q = eval("Q('bool',must =[Q('match', name = g_id), Q('terms', type = ['Group', 'Author'])])")

                # q = Q('match',name=dict(query='File',type='phrase'))
                s1 = Search(using=es, index='nodes',doc_type="node").query(q)
                s2 = s1.execute()
                group_node = s2[0]
                # group_node = node_collection.one({'_type': {'$in': ["Group", "Author"]}, 'name': g_id})

            if group_node:
                # Check whether Group is PUBLIC or not
                if not group_node.group_type == u"PUBLIC":
                    # If Group other than Public one is found

                    if user.is_authenticated():
                        # Check for user's authenticity & accessibility of the group
                        if user.is_superuser or group_node.created_by == user.id or user.id in group_node.group_admin or user.id in group_node.author_set:
                            pass

                        else:
                            error_message = "\n Something went wrong: Either url is invalid or such group/user doesn't exists !!!\n"
                            raise PermissionDenied(error_message)

                    else:
                        # Anonymous user found which cannot access groups other than Public
                        error_message = "\n Something went wrong: Either url is invalid or such group/user doesn't exists !!!\n"
                        raise PermissionDenied(error_message)

            else:
                # If Group is not found with either given ObjectId or name in the database
                # Then compare with a given list of names as these were used in one of the urls
                # And still no match found, throw error
                if g_id not in ["online", "i18n", "raw", "r", "m", "t", "new", "mobwrite", "admin", "benchmarker", "accounts", "Beta", "welcome", "explore"]:
                    error_message = "\n Something went wrong: Either url is invalid or such group/user doesn't exists !!!\n"
                    raise Http404(error_message)

        return True

    except PermissionDenied as e:
        raise PermissionDenied(e)

    except Http404 as e:
        raise Http404(e)


def get_attribute_value(node_id, attr_name, get_data_type=False, use_cache=True):
    print("in get_attribute_value")
    cache_key = str(node_id) + 'attribute_value' + str(attr_name)
    cache_result = cache.get(cache_key)

    # if (cache_key in cache) and not get_data_type and use_cache:
    #     #print "from cache in module detail:", cache_result
    #     return cache_result

    attr_val = ""
    node_attr = data_type = None
    if node_id:
        # print "\n attr_name: ", attr_name
        # gattr = node_collection.one({'_type': 'AttributeType', 'name': unicode(attr_name) })
        q = eval("Q('bool',must =[Q('match', type = 'AttributeType'), Q('match', name = attr_name)])")

        # q = Q('match',name=dict(query='File',type='phrase'))
        s1 = Search(using=es, index='nodes',doc_type="node").query(q)
        s2 = s1.execute()
        gattr = s2[0]

        if get_data_type:
            data_type = gattr.data_type
        if gattr: # and node  :

            # node_attr = triple_collection.find_one({'_type': "GAttribute", "subject": ObjectId(node_id), 'attribute_type': gattr._id, 'status': u"PUBLISHED"})
            print(node_id,gattr.id)
            q = eval("Q('bool',must =[Q('match', type = 'GAttribute'), Q('match', subject = str(node_id)), Q('match',attribute_type = str(gattr.id))])")

            # q = Q('match',name=dict(query='File',type='phrase'))
            s1 = Search(using=es, index='triples',doc_type="triple").query(q)
            s2 = s1.execute()
           # print "s2:",s2,q
            if s1.count() > 0:
                node_attr = s2[0]
                attr_val = node_attr.object_value
                #print("\n here: ", attr_name, " : ", type(attr_val), " : ", attr_val)
                #print("node attr:",node_attr)
    if get_data_type:
        return {'value': attr_val, 'data_type': data_type}
    cache.set(cache_key, attr_val, 60 * 60)
    return attr_val

def get_gst_name_id(gst_name_or_id):
    # if cached result exists return it
    print("in gst_name_or_id",gst_name_or_id)
    slug = slugify(gst_name_or_id)
    cache_key = 'gst_name_id' + str(slug)
    cache_result = cache.get(cache_key)

    if cache_result:
        return (cache_result[0], ObjectId(cache_result[1]))
    # ---------------------------------

    # gst_id = ObjectId(gst_name_or_id) if ObjectId.is_valid(gst_name_or_id) else None
    
    # gst_obj = node_collection.one({
    #                                 "_type": {"$in": ["GSystemType", "MetaType"]},
    #                                 "$or":[
    #                                     {"_id": gst_id},
    #                                     {"name": unicode(gst_name_or_id)}
    #                                 ]
    #                             })
    if isinstance(gst_name_or_id,ObjectId):
        q2 = Q('match',id=str(gst_name_or_id))
    else:
        q2 = Q('match',name=gst_name_or_id)

    q = eval("Q('bool',must =[Q('terms', type = ['GSystemType','MetaType']),q2])")

    # q = Q('match',name=dict(query='File',type='phrase'))
    s1 = Search(using=es, index='nodes',doc_type="node").query(q)
    s2 = s1.execute()
    #print "s2",s2
    gst_obj = s2[0]
    #print "Object:",gst_obj
    if gst_obj:
        gst_name = gst_obj.name
        gst_id = gst_obj.id

        # setting cache with ObjectId
        cache_key = u'gst_name_id' + str(slugify(gst_id))
        cache.set(cache_key, (gst_name, gst_id), 60 * 60)

        # setting cache with gst_name
        cache_key = u'gst_name_id' + str(slugify(gst_name))
        cache.set(cache_key, (gst_name, gst_id), 60 * 60)

        return gst_name, gst_id

    return None, None

def save_node_to_es(django_document):
    try:
        print("called to save_to_es method of es_queries")
        # node_types = ['GSystemType','MetaType','AttributeType','RelationType','GSystem']
        with open("/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/gstudio_configs/req_body.json") as req_body:
            request_body = json.load(req_body)
        
        doc = json.dumps(django_document,cls=NodeJSONEncoder)
        print("00000000000000000000000000000000000000000000000")
        print(doc)
        print("00000000000000000000000000000000000000000000000")
        django_document = json.loads(doc)
        print("=================================================")
        print(django_document)
        print("=================================================")

        django_document["id"] = django_document.pop("_id")
        django_document["type"] = django_document.pop("_cls")
        index = None

        for k in GSTUDIO_ELASTIC_SEARCH_INDEX:
            for v in GSTUDIO_ELASTIC_SEARCH_INDEX[k]:
                if django_document["type"] in v:
                    if GSTUDIO_SITE_NAME == "CLIx":            
                        doc = json.dumps(django_document,cls=NodeJSONEncoder)
                        index = k
                    else:
                        index = GSTUDIO_SITE_NAME+"_"+k
                    index = index.lower()
                    break

        print(django_document["type"])
        # if django_document["type"] == "GSystem" and GSTUDIO_SITE_NAME == "CLIx":
        #     print django_document["id"]
        #     print "-------------------------------------------------------------"
        #     es.index(index=index, doc_type="gsystem", id=django_document["id"], body=django_document)
        #     file_name.write(document["id"] + '\n')
        #     if django_document["type"]=="GSystem":
        #         if('if_file' in django_document.keys()):
        #             if(django_document["if_file"]["mime_type"] is not None):
        #                 data = django_document["if_file"]["mime_type"].split("/")
        #                 doc_type = data[0]
        #             else:
        #                 doc_type = "notmedia"
        #         else:
        #             doc_type = "notmedia"

        #     else:
        #         doc_type = "dontcare"

        #     if (not es.indices.exists("gsystem")):
        #         res = es.indices.create(index="gsystem", body=request_body)
        #     es.index(index="gsystem", doc_type=doc_type, id=django_document["id"], body=django_document)

        # else:
        #     print django_document["id"]
        #     if (not es.indices.exists("benchmarks")):
        #         res = es.indices.create(index="benchmarks", body=benchmarks_body)

        es.index(index='nodes', doc_type='node', id=django_document["id"], body=django_document)

    except Exception as e:
        print("Error while saving data to ES: "+str(e))


def save_triple_to_es(django_document):
    try:
        print("called to save_to_es method of es_queries")
        # node_types = ['GSystemType','MetaType','AttributeType','RelationType','GSystem']
        with open("/home/docker/code/clixoer/gnowsys-ndf/gnowsys_ndf/gstudio_configs/triples.json") as req_body:
            request_body = json.load(req_body)
        
        doc = json.dumps(django_document,cls=NodeJSONEncoder)
        print("00000000000000000000000000000000000000000000000")
        print(doc)
        print("00000000000000000000000000000000000000000000000")
        django_document = json.loads(doc)
        print("=================================================")
        print(django_document)
        print("=================================================")

        django_document["id"] = django_document.pop("_id")
        django_document["type"] = django_document.pop("_cls")

        index = None

        for k in GSTUDIO_ELASTIC_SEARCH_INDEX:
            for v in GSTUDIO_ELASTIC_SEARCH_INDEX[k]:
                if django_document["type"] in v:
                    if GSTUDIO_SITE_NAME == "CLIx":            
                        doc = json.dumps(django_document,cls=NodeJSONEncoder)
                        index = k
                    else:
                        index = GSTUDIO_SITE_NAME+"_"+k
                    index = index.lower()
                    break

        print(django_document["type"])
        # if django_document["type"] == "GSystem" and GSTUDIO_SITE_NAME == "CLIx":
        #     print django_document["id"]
        #     print "-------------------------------------------------------------"
        #     es.index(index=index, doc_type="gsystem", id=django_document["id"], body=django_document)
        #     file_name.write(document["id"] + '\n')
        #     if django_document["type"]=="GSystem":
        #         if('if_file' in django_document.keys()):
        #             if(django_document["if_file"]["mime_type"] is not None):
        #                 data = django_document["if_file"]["mime_type"].split("/")
        #                 doc_type = data[0]
        #             else:
        #                 doc_type = "notmedia"
        #         else:
        #             doc_type = "notmedia"

        #     else:
        #         doc_type = "dontcare"

        #     if (not es.indices.exists("gsystem")):
        #         res = es.indices.create(index="gsystem", body=request_body)
        #     es.index(index="gsystem", doc_type=doc_type, id=django_document["id"], body=django_document)

        # else:
        #     print django_document["id"]
        #     if (not es.indices.exists("benchmarks")):
        #         res = es.indices.create(index="benchmarks", body=benchmarks_body)

        es.index(index='triples', doc_type='triple', id=django_document["id"], body=django_document)

    except Exception as e:
        print("Error while saving data to ES: "+str(e))

def save_course_page(request, group_id):
    group_obj = get_group_name_id(group_id, get_obj=True)
    group_id = group_obj.id
    group_name = group_obj.name
    print("es_queries in save page",group_id,group_name)
    tags = request.POST.get("tags",[])
    if tags:
        tags = json.loads(tags)
    else:
        tags = []    
    #template = 'ndf/gevent_base.html'
    template = 'ndf/lms.html'
    if not True:
        testimony_gst_name, testimony_gst_id = GSystemType.get_gst_name_id("testimony")
        testimony_obj = None
        activity_lang =  request.POST.get("lan", '')
        if request.method == "POST":
            name = request.POST.get("name", "")
            alt_name = request.POST.get("alt_name", "")
            content = request.POST.get("content_org", None)
            node_id = request.POST.get("node_id", "")
            if node_id:
                testimony_obj = node_collection.one({'_id': ObjectId(node_id)})
                if testimony_obj.altnames != alt_name:
                    testimony_obj.altnames = unicode(alt_name)
            else:
                # is_info_testimony = request.POST.get("testimony_type", "")
                testimony_obj = GSystem()
                testimony_obj.fill_gstystem_values(request=request)
                testimony_obj.member_of = [testimony_gst_id]
                testimony_obj.altnames = unicode(alt_name)
                # if is_info_testimony == "Info":
                #     info_testimony_gst_name, info_testimony_gst_id = GSystemType.get_gst_name_id('Info testimony')
                #     testimony_obj.type_of = [info_testimony_gst_id]
            
            if activity_lang:
                language = get_language_tuple(activity_lang)
                testimony_obj.language = language
            # if 'admin_info_page' in request.POST:
            #     admin_info_page = request.POST['admin_info_page']
            #     if admin_info_page:
            #         admin_info_page = json.loads(admin_info_page)
            #     if "None" not in admin_info_page:
            #         has_admin_rt = node_collection.one({'_type': "RelationType", 'name': "has_admin_page"})
            #         admin_info_page = map(ObjectId, admin_info_page)
            #         create_grelation(page_obj._id, has_admin_rt,admin_info_page)
            #         page_obj.reload()
            #     return HttpResponseRedirect(reverse("view_course_page",
            #      kwargs={'group_id': group_id, 'page_id': page_obj._id}))

            # if 'help_info_page' in request.POST:
            #     help_info_page = request.POST['help_info_page']
            #     if help_info_page:
            #         help_info_page = json.loads(help_info_page)
            #     if "None" not in help_info_page:
            #         has_help_rt = node_collection.one({'_type': "RelationType", 'name': "has_help"})
            #         help_info_page = map(ObjectId, help_info_page)
            #         create_grelation(page_obj._id, has_help_rt,help_info_page)
            #         page_obj.reload()
            #     return HttpResponseRedirect(reverse("view_course_page",
            #      kwargs={'group_id': group_id, 'page_id': page_obj._id}))
            testimony_obj.fill_gstystem_values(tags=tags)
            testimony_obj.name = unicode(name)
            testimony_obj.content = unicode(content)
            testimony_obj.created_by = request.user.id
            testimony_obj.save(groupid=group_id)
            return HttpResponseRedirect(reverse("view_course_page",
             kwargs={'group_id': group_id, 'page_id': testimony_obj.id}))
    else:
        page_gst_name, page_gst_id = get_gst_name_id("Page")
        page_obj = None
        activity_lang =  request.POST.get("lan", '')
        if request.method == "POST":
            name = request.POST.get("name", "")
            alt_name = request.POST.get("alt_name", "")
            content = request.POST.get("content_org", None)
            node_id = request.POST.get("node_id", "")
            if node_id:
                page_obj = node_collection.one({'_id': ObjectId(node_id)})
                q = eval("Q('match', id = str(node_id))")

                # q = Q('match',name=dict(query='File',type='phrase'))
                s1 = Search(using=es, index='nodes',doc_type="node").query(q)
                s2 = s1.execute()
                if page_obj.altnames != alt_name:
                    page_obj.altnames = unicode(alt_name)
            else:
                is_info_page = request.POST.get("page_type", "")
                page_obj = node_collection.collection.GSystem()
                page_obj.fill_gstystem_values(request=request)
                page_obj.member_of = [page_gst_id]
                page_obj.altnames = unicode(alt_name)
                
            
            if activity_lang:
                language = get_language_tuple(activity_lang)
                page_obj.language = language
            
            page_obj.fill_gstystem_values(tags=tags)
            page_obj.name = unicode(name)
            page_obj.content = unicode(content)
            page_obj.created_by = request.user.id
            page_obj.save(groupid=group_id)
            print("page_object saved:",page_obj)
            save_node_to_es(page_obj)
            return HttpResponseRedirect(reverse("view_course_page",
             kwargs={'group_id': group_id, 'page_id': page_obj.id}))


def module_detail(request, group_id, node_id,title=""):
    '''
    detail of of selected module
    '''
    group_name, group_id = Group.get_group_name_id(group_id)
    print("in module_detail and group id, title",group_id,title)
    print("node_id",node_id)          
    module_obj = Node.get_node_by_id(ObjectId(node_id))
    context_variable = {
                        'group_id': group_id, 'groupid': group_id,
                        'node': module_obj, 'title': title,
                        'card': 'ndf/event_card.html', 'card_url_name': 'groupchange'
                    }

    #gstaff_access = check_is_gstaff(group_id,request.user)
    primary_lang_tuple = get_language_tuple(GSTUDIO_PRIMARY_COURSE_LANGUAGE)
    if title == "courses":

        module_detail_query = Q('bool',must = [Q('match',status = 'PUBLISHED'),Q('terms',module_obj.collection_set)],\
            should=[Q('match',group_admin =request.user.id),Q('match',created_by =request.user.id),Q('match',author_set =request.user.id),Q('match',member_of =gst_ce_id),Q('match',member_of =gst_announced_unit_id),\
            Q('match',group_type ='PUBLIC'),Q('match',language=primary_lang_tuple),Q('match',member_of=gst_ce_id)],minimum_should_match=1)
    
    if title == "drafts":
        module_detail_query.update({'$or': [
        {'$and': [
            {'member_of': gst_base_unit_id},
            {'$or': [
              {'created_by': request.user.id},
              {'group_admin': request.user.id},
              {'author_set': request.user.id},
            ]}
        ]},
      ]}) 

    # units_under_module = Node.get_nodes_by_ids_list(module_obj.collection_set)
    '''
    gstaff_access = check_is_gstaff(group_id, request.user)

    if gstaff_access:
        module_detail_query.update({'member_of': {'$in': [gst_announced_unit_id, gst_base_unit_id]}})
    else:
        module_detail_query.update({'member_of': gst_announced_unit_id})
    '''
    units_under_module = node_collection.find(module_detail_query).sort('last_update', -1)
    context_variable.update({'units_under_module': units_under_module})

    units_sort_list = get_attribute_value(node_id, 'items_sort_list')
    from django.core.cache import cache
    #test = cache.get('5945db6e2c4796014abd1784attribute_valueitems_sort_list')
    #print "test:",test 
    if units_sort_list:
        #print "from attribute:",units_sort_list
        context_variable.update({'units_sort_list': units_sort_list})
    else:
        print("no items_sort_list")
        context_variable.update({'units_sort_list': list(units_under_module)})

    template = 'ndf/module_detail.html'
    #print "units of selected module", units_sort_list
    return render_to_response(
        template,
        context_variable,
        context_instance=RequestContext(request))

def member_of_names_list(group_obj):
        """Returns a list having names of each member (GSystemType, i.e Page,
        File, etc.), built from 'member_of' field (list of ObjectIds)

        """
        # from gsystem_type import GSystemType
        return [get_gst_name_id(ObjectId(gst_id))[0] for gst_id in group_obj.member_of]

def _get_current_and_old_display_pics(group_obj):

    # has_banner_pic_rt = node_collection.one({'_type': 'RelationType', 'name': unicode('has_banner_pic') })

    q = Q('bool',must=[Q('match', type = 'RelationType'),Q('match',name = 'has_banner_pic')])

    # q = Q('match',name=dict(query='File',type='phrase'))
    s1 = Search(using=es, index='nodes',doc_type="node").query(q)
    s2 = s1.execute()
    has_banner_pic_rt = s2[0]

    banner_pic_obj = None
    old_profile_pics = []
    for each in group_obj.relation_set:
        if "has_banner_pic" in each:
            # banner_pic_obj = node_collection.one(
            #     {'_type': {'$in':     activity_gst_name, activity_gst_id = get_gst_name_id("activity")
            #       ["GSystem", "File"]}, '_id': each["has_banner_pic"]}
            # )
            q = Q('bool',must=[Q('match', id = str(each["has_banner_pic"])),Q('terms',type = ["GSystem", "File"])])

            # q = Q('match',name=dict(query='File',type='phrase'))
            s1 = Search(using=es, index='nodes',doc_type="node").query(q)
            s2 = s1.execute()
            banner_pic_obj = s2[0]
            break

    # all_old_prof_pics = triple_collection.find({'_type': "GRelation", "subject": group_obj._id, 'relation_type': has_banner_pic_rt._id, 'status': u"DELETED"})
    
    q = Q('bool',must=[Q('match', type = 'GRelation'), Q('match', subject = str(group_obj.id)), Q('match', relation_type = str(has_banner_pic_rt.id))])
    s1 = Search(using=es, index='triples',doc_type="triple").query(q)

    # print "s1:",s1,q
    all_old_prof_pics = s1.execute()

    if all_old_prof_pics:
        for each_grel in all_old_prof_pics:
            if each_grel.status == 'DELETED':
                # n = node_collection.one({'_id': ObjectId(each_grel.right_subject)})
                q = Q('bool',must=[Q('match', id = each_grel.right_subject)])

                # q = Q('match',name=dict(query='File',type='phrase'))
                s1 = Search(using=es, index='nodes',doc_type="node").query(q)
                s2 = s1.execute()
                n = s2[0]
                if n not in old_profile_pics:
                    old_profile_pics.append(n)

    return banner_pic_obj, old_profile_pics


def course_content(request, group_id):
    print("es_queries : In course_content",group_id, request.LANGUAGE_CODE)
    group_obj   = get_group_name_id(group_id, get_obj=True)
    list_of_memberof_name = member_of_names_list(group_obj)
    group_id    = group_obj.id
    group_name  = group_obj.name
    allow_to_join = get_group_join_status(group_obj)
    template = 'ndf/gcourse_event_group.html'
    unit_structure =  get_course_content_hierarchy(group_obj,request.LANGUAGE_CODE)
    print("unit_structure:",unit_structure)
    visited_nodes = []
    if 'BaseCourseGroup' in list_of_memberof_name:
        template = 'ndf/basecourse_group.html'
    if 'base_unit' in list_of_memberof_name:
        template = 'ndf/lms.html'
    if 'announced_unit' in list_of_memberof_name or 'Group' in list_of_memberof_name or 'Author' in list_of_memberof_name and 'base_unit' not in list_of_memberof_name:
        template = 'ndf/lms.html'
    banner_pic_obj,old_profile_pics = _get_current_and_old_display_pics(group_obj)
    # if request.user.is_authenticated():
    #     counter_obj = Counter.get_counter_obj(request.user.id, ObjectId(group_id))
    #     if counter_obj:
    #         # visited_nodes = map(str,counter_obj['visited_nodes'].keys())
    #         #print counter_obj
    #         visited_nodes = counter_obj['visited_nodes']
    print("banner_pic_obj:",banner_pic_obj)
    context_variables = RequestContext(request, {
            'group_id': group_id, 'groupid': group_id, 'group_name':group_name,
            'group_obj': group_obj,'node': group_obj, 'title': 'course content',
            'allow_to_join': allow_to_join,
            'old_profile_pics':old_profile_pics, "prof_pic_obj": banner_pic_obj,
            'unit_structure': json.dumps(unit_structure,cls=NodeJSONEncoder),
            'visited_nodes': json.dumps(visited_nodes)
            })
    print("Before rendering template",template)
    return render_to_response(template, context_variables)

def get_name_id_from_type(node_name_or_id, node_type, get_obj=False):
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
    # node_obj = node_collection.one({
    #                                 "_type": {"$in": [
    #                                         # "GSystemType",
    #                                         # "MetaType",
    #                                         # "RelationType",
    #                                         # "AttributeType",
    #                                         # "Group",
    #                                         # "Author",
    #                                         node_type
    #                                     ]},
    #                                 "$or":[
    #                                     {"_id": node_id},
    #                                     {"name": unicode(node_name_or_id)}
    #                                 ]
    #                             })

    if ObjectId.is_valid(node_name_or_id):

        q = Q('bool',must=[Q('match', type = node_type),Q('match',id=str(node_name_or_id))])
    else:
        q = Q('bool',must=[Q('match', type = node_type),Q('match',name=node_name_or_id)])

    # q = Q('match',name=dict(query='File',type='phrase'))
    s1 = Search(using=es, index='nodes',doc_type="node").query(q)
    s2 = s1.execute()
    node_obj =s2[0]


    if node_obj:
        node_name = node_obj.name
        node_id = node_obj.id

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


def course_pages(request, group_id, page_id=None,page_no=1):
    from gnowsys_ndf.settings import GSTUDIO_NO_OF_OBJS_PP
    group_obj = get_group_name_id(group_id, get_obj=True)
    page_gst_name, page_gst_id = get_gst_name_id("Page")
    group_id = group_obj.id
    group_name = group_obj.name
    #template = 'ndf/gevent_base.html'
    print("inside course_pages",group_id)
    template = 'ndf/lms.html'
    context_variables = {
            'group_id': group_id, 'groupid': group_id, 'group_name':group_name,
            'group_obj': group_obj, 'title': 'course_pages',
            'editor_view': True, 'activity_node': None, 'all_pages': None}

    if page_id:
        q = Q('bool',must=[Q('match', id = str(page_id))])

        # q = Q('match',name=dict(query='File',type='phrase'))
        s1 = Search(using=es, index='nodes',doc_type="node").query(q)
        s2 = s1.execute()
        node_obj =s2[0]
        rt_translation_of = get_name_id_from_type('translation_of', 'RelationType', get_obj=True)
        # other_translations_grels = triple_collection.find({
        #                     '_type': u'GRelation',
        #                     'subject': ObjectId(page_id),
        #                     'relation_type': rt_translation_of._id,
        #                     'right_subject': {'$nin': [node_obj._id]}
        #                 })

        q = Q('bool',must=[Q('match', type='GRelation'),Q('match',subject=str(page_id)),Q('match',relation_type=rt_translation_of.id)],must_not = [Q('match', right_subject = str(node_obj.id))])

        # q = Q('match',name=dict(query='File',type='phrase'))
        s1 = Search(using=es, index='triples',doc_type="triple").query(q)
        other_translations_grels = s1.execute()
        # node_obj =s2[0]
        rgtsubjects_list = [r.right_subject for r in other_translations_grels]
        
        # other_translations = node_collection.find({'_id': {'$in': [r.right_subject for r in other_translations_grels]} })
        q = Q('terms',id = rgtsubjects_list)
        # q = Q('match',name=dict(query='File',type='phrase'))
        s1 = Search(using=es, index='triples',doc_type="triple").query(q)
        other_translations = s1.execute()
        
        context_variables.update({'activity_node': node_obj, 'hide_breadcrumbs': True,'other_translations':other_translations})
        context_variables.update({'editor_view': False})

    else:
        activity_gst_name, activity_gst_id = get_gst_name_id("activity")
        # all_pages = node_collection.find({'member_of':
        #             {'$in': [page_gst_id, activity_gst_id] }, 'group_set': group_id,
        #             'type_of': {'$ne': [blog_page_gst_id]}
        #             # 'content': {'$regex': 'clix-activity-styles.css', '$options': 'i'}
        #             }).sort('last_update',-1)
        
        q = Q('bool',must = [Q('terms',member_of = [str(page_gst_id), str(activity_gst_id)]),Q('match',group_set = group_id)])

        # q = Q('match',name=dict(query='File',type='phrase'))
        s1 = Search(using=es, index='nodes',doc_type="node").query(q).sort('-last_update')
        all_pages = s1.execute()



        course_pages_info = Paginator(all_pages, page_no, GSTUDIO_NO_OF_OBJS_PP)
        context_variables.update({'editor_view': False, 'all_pages': all_pages,'course_pages_info':course_pages_info})
    return render_to_response(template,
                                context_variables,
                                context_instance = RequestContext(request)
    )

def create_edit_course_page(request, group_id, page_id=None,page_type=None):
    #print "es_queries inside create_edit_activity",group_id
    group_obj = get_group_name_id(group_id, get_obj=True)
    group_id = group_obj.id
    group_name = group_obj.name
    #template = 'ndf/gevent_base.html'
    template = 'ndf/lms.html'
    # templates_gst = node_collection.one({"_type":"GSystemType","name":"Template"})
    # if templates_gst._id:
    #   # templates_cur = node_collection.find({"member_of":ObjectId(GST_PAGE._id),"type_of":ObjectId(templates_gst._id)})
    #   templates_cur = node_collection.find({"type_of":ObjectId(templates_gst._id)})

    context_variables = {
            'group_id': group_id, 'groupid': group_id, 'group_name':group_name,'page_type':page_type,
            'group_obj': group_obj, 'title': 'create_course_pages',
            'activity_node': None, #'templates_cur': templates_cur,
            'cancel_activity_url': reverse('course_pages',
                                        kwargs={
                                        'group_id': group_id
                                        })}

    if page_id:
        # node_obj = node_collection.one({'_id': ObjectId(page_id)})
        q = Q('bool',must=[Q('match', id = page_id)])

        # q = Q('match',name=dict(query='File',type='phrase'))
        s1 = Search(using=es, index='nodes',doc_type="node").query(q)
        s2 = s1.execute()
        node_obj =s2[0]

        context_variables.update({'activity_node': node_obj, 'hide_breadcrumbs': True,
            'cancel_activity_url': reverse('view_course_page',
                                        kwargs={
                                        'group_id': group_id,
                                        'page_id': node_obj.id
                                        })})


    return render_to_response(template,
                                context_variables,
                                context_instance = RequestContext(request)
    )

def get_group_join_status(group_obj):
    # from gnowsys_ndf.ndf.templatetags.ndf_tags import get_attribute_value
    allow_to_join = None
    start_enrollment_date = get_attribute_value(group_obj.id,"start_enroll")
    last_enrollment_date = get_attribute_value(group_obj.id,"end_enroll")
    curr_date_time = datetime.datetime.now().date()
    print("start_enroll:",start_enrollment_date)
    print("end_enroll:",last_enrollment_date)
    if start_enrollment_date and last_enrollment_date:
      start_enrollment_date = datetime.datetime.strptime(start_enrollment_date, '%d/%m/%Y %H:%M:%S:%f')
      last_enrollment_date = datetime.datetime.strptime(last_enrollment_date, '%d/%m/%Y %H:%M:%S:%f')
      start_enrollment_date = start_enrollment_date.date()
      last_enrollment_date = last_enrollment_date.date()
      if start_enrollment_date <= curr_date_time and last_enrollment_date >= curr_date_time:
          allow_to_join = "Open"
      else:
          allow_to_join = "Closed"
    return allow_to_join

def get_course_content_hierarchy(unit_group_obj,lang="en"):
    '''
    ARGS: unit_group_obj
    Result will be of following form:
    {
        name: 'Lesson1',
        type: 'lesson',
        id: 'l1',
        activities: [
            {
                name: 'Activity 1',
                type: 'activity',
                id: 'a1'
            },
            {
                name: 'Activity 1',
                type: 'activity',
                id: 'a2'
            }
        ]
    }, {
        name: 'Lesson2',
        type: 'lesson',
        id: 'l2',
        activities: [
            {
                name: 'Activity 1',
                type: 'activity',
                id: 'a1'
            }
        ]
    }
    '''

    unit_structure = []
    for each in unit_group_obj.collection_set:
        lesson_dict ={}
        lesson = get_node_by_id(each)

        if lesson:
            trans_lesson = get_lang_node(lesson.id,lang)
            print("lesson:",lesson.name)
            if trans_lesson:
                print("inside trans")
                lesson_dict['label'] = str(trans_lesson.name).encode('utf-8')
                lesson_dict['id'] = trans_lesson.id
            else:
                lesson_dict['label'] = lesson.name
                lesson_dict['id'] = lesson.id
            lesson_dict['type'] = 'unit-name'
            lesson_dict['children'] = []
            if lesson.collection_set:
                for each_act in lesson.collection_set:
                    activity_dict ={}
                    activity = get_node_by_id(each_act)
                    if activity:
                        trans_act_name = get_lang_node(each_act,lang)
                        # activity_dict['label'] = trans_act_name.name or activity.name  
                        if trans_act_name:
                            activity_dict['label'] =str(trans_act_name.name).encode('utf-8')
                            activity_dict['id'] = str(trans_act_name.id)
                            print("in side activity loop", trans_act_name.id, "in language", lang)
                            #activity_dict['label'] = trans_act_name.name
                        else:
                            activity_dict['label'] = activity.name
                            activity_dict['id'] = str(activity.id)
                            #activity_dict['label'] = activity.altnames or activity.name
                        activity_dict['type'] = 'activity-group'
                        #activity_dict['id'] = str(activity.id)
                        lesson_dict['children'].append(activity_dict)
            unit_structure.append(lesson_dict)
    return unit_structure

def get_lang_node(node_id,lang):
    rel_value = get_relation_value(node_id,"translation_of")
    #print "rel_value node:",rel_value,node_id
    if 'grel_node' in rel_value:
        for each in rel_value['grel_node']:
            if each.language[0] ==  get_language_tuple(lang)[0]:
                trans_node = each
                #print "in get_lang_node", trans_node.id, "in language", each.language[0]
                trnsnd = get_node_by_id(trans_node)
                return trnsnd
    else:
        return ""

def get_language_tuple(lang):
    """
    from input argument of language code of language name
    get the std matching tuple from settings.

    Returns:
        tuple: (<language code>, <language name>)

    Args:
        lang (str or unicode): it is the one of item from tuple.
        It may either language-code or language-name.
    """
    if not lang:
        return ('en', 'English')

    all_languages = list(LANGUAGES)# + OTHER_COMMON_LANGUAGES

    # check if lang argument itself is a complete, valid tuple that exists in all_languages.
    if (lang in all_languages) or (tuple(lang) in all_languages):
        return lang

    all_languages_concanated = reduce(lambda x, y: x+y, all_languages)

    # iterating over each document in the cursor:
    # - Secondly, replacing invalid language values to valid tuple from settings
    if lang in all_languages_concanated:
        for each_lang in all_languages:
            if lang in each_lang:
                return each_lang

    # as a default return: ('en', 'English')
    return ('en', 'English')

def get_relation_value(node_id, grel, return_single_right_subject=False):

    # import ipdb; ipdb.set_trace()
    try:
        result_dict = {}
        if node_id:
            # node = node_collection.one({'_id': ObjectId(node_id) })
            node = get_node_by_id(node_id)
            # relation_type_node = node_collection.one({'_type': 'RelationType', 'name': unicode(grel) })
            q = eval("Q('bool',must=[Q('match', type = 'RelationType'), Q('match', name = grel)])")

            # q = Q('match',name=dict(query='File',type='phrase'))
            s1 = Search(using=es, index='nodes',doc_type="node").query(q)
            s2 = s1.execute()
            relation_type_node = s2[0]
            print("relation_type_node.object_cardinality:",relation_type_node.id,relation_type_node.object_cardinality)
            if node and relation_type_node:
                if relation_type_node.object_cardinality and relation_type_node.object_cardinality > 1:
                    # node_grel = triple_collection.find({'_type': "GRelation", "subject": node._id, 'relation_type': relation_type_node._id,'status':"PUBLISHED"})
                    q = Q('bool',must=[Q('match', type = 'GRelation'), Q('match', subject = str(node.id)), Q('match', relation_type = str(relation_type_node.id))])
                    s1 = Search(using=es, index='triples',doc_type="triple").query(q)
                    # print "s1:",s1,q
                    s2 = s1.execute()
                    # print "tripl nds:",s2
                    node_grel = s2

                    if node_grel:
                        grel_val = []
                        grel_id = []
                        for each_node in node_grel:
                            grel_val.append(each_node.right_subject)
                            grel_id.append(each_node.id)
                        # grel_val_node_cur = node_collection.find({'_id':{'$in' : grel_val}})

                        q = Q('terms', id = grel_val)

                        # q = Q('match',name=dict(query='File',type='phrase'))
                        s1 = Search(using=es, index='nodes',doc_type="node").query(q)
                        grel_val_node_cur = s1.execute()

                        result_dict.update({"cursor": True})
                        if return_single_right_subject:
                            # grel_val_node_cur = node_collection.find_one({'_id':{'$in' : grel_val}})
                            q = Q('match', id = grel_val)

                            # q = Q('match',name=dict(query='File',type='phrase'))
                            s1 = Search(using=es, index='nodes',doc_type="node").query(q)
                            s2 = s1.execute()
                            grel_val_node_cur = s2[0]                            
                            result_dict.update({"cursor": False})
                        # nodes = [grel_node_val for grel_node_val in grel_val_node_cur]
                        # print "\n\n grel_val_node, grel_id == ",grel_val_node, grel_id
                        result_dict.update({"grel_id": grel_id, "grel_node": grel_val_node_cur})
                else:
                    #print "else:",grel
                    # node_grel = triple_collection.one({'_type': "GRelation", "subject": node._id, 'relation_type': relation_type_node._id,'status':"PUBLISHED"})
                    q = Q('bool',must=[Q('match', type = 'GRelation'), Q('match', subject = node_id), Q('match', relation_type = relation_type_node.id)])
                    s1 = Search(using=es, index='triples',doc_type="triple").query(q)
                    s2 = s1.execute()
                    for each in s1[0:s1.count()]:
                        if each.status == 'PUBLISHED':
                            node_grel = each
                            break
                
                    if node_grel:
                        grel_val = list()
                        grel_val = node_grel.right_subject
                        grel_val = grel_val if isinstance(grel_val, list) else grel_val
                        grel_id = node_grel.id
                        # grel_val_node = node_collection.one({'_id':ObjectId(grel_val)})
                        # grel_val_node = node_collection.find_one({'_id':{'$in': grel_val}})

                        q = Q('match', id = grel_val)
                        # q = Q('match',name=dict(query='File',type='phrase'))
                        s1 = Search(using=es, index='nodes',doc_type="node").query(q)
                        s2 = s1.execute()
                        grel_val_node = s2[0]
                        
                        # returns right_subject of grelation and GRelation _id
                        result_dict.update({"grel_id": grel_id, "grel_node": grel_val_node, "cursor": False})
        print("\n\nresult_dict === ",result_dict)
        return result_dict
    except Exception as e:
        print(e)
        return {}

def get_unit_hierarchy(unit_group_obj,lang="en"):
    '''
    ARGS: unit_group_obj
    Result will be of following form:
    {
        name: 'Lesson1',
        type: 'lesson',
        id: 'l1',
        activities: [
            {
                name: 'Activity 1',
                type: 'activity',
                id: 'a1'
            },
            {
                name: 'Activity 1',
                type: 'activity',
                id: 'a2'
            }
        ]
    }, {
        name: 'Lesson2',
        type: 'lesson',
        id: 'l2',
        activities: [
            {
                name: 'Activity 1',
                type: 'activity',
                id: 'a1'
            }
        ]
    }
    '''
    unit_structure = []
    print("unit object and collection_set:",unit_group_obj.name,unit_group_obj.collection_set)
    for each in unit_group_obj.collection_set:
        lesson_dict ={}
        lesson = get_node_by_id(str(each))
        if lesson:
            print("1 lesson:",lesson.name)
            if lang != 'en':
                trans_lesson = get_lang_node(lesson.id,lang)
                lesson_dict['name'] = trans_lesson.name
                lesson_dict['id'] = str(trans_lesson.id)
                lesson_dict['language'] = trans_lesson.language[0]
                print("\t 2 trans lesson:",str(trans_lesson.name).encode('utf-8'),trans_lesson.id,trans_lesson.language[0])
            else:
                lesson_dict['name'] = lesson.name
                lesson_dict['id'] = str(lesson.id)
            lesson_dict['type'] = 'lesson'
            #lesson_dict['id'] = str(lesson.id)
            #lesson_dict['language'] = lesson.language[0]
            lesson_dict['activities'] = []
            if lesson.collection_set:
                for each_act in lesson.collection_set:
                    activity_dict ={}
                    activity = Node.get_node_by_id(each_act)
                    if activity:
                        trans_act = get_lang_node(activity.id,lang)
                        if trans_act:
                            # activity_dict['name'] = trans_act.name
                            activity_dict['name'] = trans_act.altnames or trans_act.name
                            activity_dict['id'] = str(trans_act.id)
                            print("\t \t 3 trans act:",str(trans_act.name).encode('utf-8'),trans_act.id)
                        else:
                            # activity_dict['name'] = activity.name
                            activity_dict['id'] = str(activity.id)
                            activity_dict['name'] = activity.altnames or activity.name
                        activity_dict['type'] = 'activity'
                        #activity_dict['id'] = str(activity.id)
                        lesson_dict['activities'].append(activity_dict)
            unit_structure.append(lesson_dict)
    return unit_structure

def unit_detail(request, group_id):
    '''
    detail of of selected units
    '''
    # parent_group_name, parent_group_id = Group.get_group_name_id(group_id)
    print("es_queries : In unit-detail ",group_id)
    unit_group_obj = get_group_name_id(group_id, get_obj=True)
    unit_structure = get_unit_hierarchy(unit_group_obj, request.LANGUAGE_CODE)
    # template = "ndf/unit_structure.html"
    # template = 'ndf/gevent_base.html'
    template = 'ndf/lms.html'

    # print unit_structure
    req_context = RequestContext(request, {
                                'title': 'unit_authoring',
                                'hide_bannerpic': True,
                                'group_id': unit_group_obj.id,
                                'groupid': unit_group_obj.id,
                                'group_name': unit_group_obj.name,
                                'unit_obj': unit_group_obj,
                                'group_obj': unit_group_obj,
                                'unit_structure': json.dumps(unit_structure)
                            })
    return render_to_response(template, req_context)

def lesson_create_edit(request, group_id, unit_group_id=None):
    '''
    creation as well as edit of lessons
    returns following:
    {
        'success': <BOOL: 0 or 1>,
        'unit_hierarchy': <unit hierarchy json>,
        'msg': <error msg or objectid of newly created obj>
    }
    '''
    # parent_group_name, parent_group_id = Group.get_group_name_id(group_id)

    # parent unit id

    gst_lesson_name, gst_lesson_id = get_gst_name_id('lesson')
    gst_activity_name, gst_activity_id = get_gst_name_id('activity')
    gst_module_name, gst_module_id = get_gst_name_id('Module')
    rt_translation_of = get_name_id_from_type('translation_of', 'RelationType', get_obj=True)


    lesson_id = request.POST.get('lesson_id', None)
    lesson_language = request.POST.get('sel_lesson_lang','')
    unit_id_post = request.POST.get('unit_id', '')
    lesson_content = request.POST.get('lesson_desc', '')
    # print "lesson_id: ", lesson_id
    # print "lesson_language: ", lesson_language
    # print "unit_id_post: ", unit_id_post
    unit_group_id = unit_id_post if unit_id_post else unit_group_id
    # getting parent unit object
    unit_group_obj = Group.get_group_name_id(unit_group_id, get_obj=True)
    result_dict = {'success': 0, 'unit_hierarchy': [], 'msg': ''}
    if request.method == "POST":
        # lesson name
        lesson_name = request.POST.get('name', '').strip()
        if not lesson_name:
            msg = 'Name can not be empty.'
            result_dict = {'success': 0, 'unit_hierarchy': [], 'msg': msg}
            # return HttpResponse(0)

        # check for uniqueness of name
        # unit_cs: unit collection_set
        unit_cs_list = [str(each) for each in unit_group_obj.collection_set]
        print("unit list:",unit_cs_list)
        unit_cs_objs_cur = get_nodes_by_ids_list(unit_cs_list)
        if unit_cs_objs_cur:
            unit_cs_names_list = [u.name for u in unit_cs_objs_cur]

        if not lesson_id and unit_cs_objs_cur  and  lesson_name in unit_cs_names_list:  # same name activity
            # currently following logic was only for "en" nodes.
            # commented and expecting following in future:
            # check for uniqueness w.r.t language selected within all sibling lessons's translated nodes

            # lesson_obj = Node.get_node_by_id(lesson_id)
            # if lesson_language != lesson_obj.language[0]:
            #     if lesson_language:
            #         language = get_language_tuple(lesson_language)
            #         lesson_obj.language = language
            #         lesson_obj.save()
            msg = u'Activity with same name exists in lesson: ' + unit_group_obj.name
            result_dict = {'success': 0, 'unit_hierarchy': [], 'msg': msg}

        elif lesson_id and ObjectId.is_valid(lesson_id):  # Update
            # getting default, "en" node:
            if lesson_language != "en":
                node = translated_node_id = None
                # grel_node = triple_collection.one({
                #                         '_type': 'GRelation',
                #                         'subject': ObjectId(lesson_id),
                #                         'relation_type': rt_translation_of._id,
                #                         'language': get_language_tuple(lesson_language),
                #                         # 'status': 'PUBLISHED'
                #                     })

                q = Q('bool',must = [Q('match',type = 'GRelation'),Q('match',subject=str(lesson_id)),Q('match',relation_type = str(rt_translation_of.id)),Q('match',language=get_language_tuple(lesson_language))])
                s1 = Search(using=es, index='triples',doc_type="triple").query(q)
                s2 = s1.execute()
                grel_node = s2[0]
                if grel_node:
                    # grelation found.
                    # transalated node exists.
                    # edit of existing translated node.

                    # node = Node.get_node_by_id(grel_node.right_subject)
                    # translated_node_id = node._id
                    lesson_id = grel_node.right_subject
                else:
                    # grelation NOT found.
                    # create transalated node.
                    user_id = request.user.id
                    new_lesson_obj = node_collection.collection.GSystem()
                    new_lesson_obj.fill_gstystem_values(name=lesson_name,
                                                    content=lesson_content,
                                                    member_of=gst_lesson_id,
                                                    group_set=unit_group_obj.id,
                                                    created_by=user_id,
                                                    status=u'PUBLISHED')
                    # print new_lesson_obj
                    if lesson_language:
                        language = get_language_tuple(lesson_language)
                        new_lesson_obj.language = language
                    new_lesson_obj.save(groupid=group_id)
                    save_node_to_es(new_lesson_obj)
                    trans_grel_list = [new_lesson_obj.id]
                    # trans_grels = triple_collection.find({'_type': 'GRelation', \
                    #         'relation_type': rt_translation_of._id,'subject': ObjectId(lesson_id)},{'_id': 0, 'right_subject': 1})
                    q = Q('bool',must = [Q('match',type = 'GRelation'),Q('match',subject=str(lesson_id)),Q('match',relation_type = str(rt_translation_of.id))])
                    s1 = Search(using=es, index='triples',doc_type="triple").query(q)
                    trans_grels = s1.execute()
                    # grel_node = s2[0]

                    for each_rel in trans_grels:
                        trans_grel_list.append(each_rel['right_subject'])
                    # translate_grel = create_grelation(node_id, rt_translation_of, trans_grel_list, language=language)
                    create_grelation(lesson_id, rt_translation_of, trans_grel_list, language=language)

            lesson_obj = Node.get_node_by_id(lesson_id)
            if lesson_obj and (lesson_obj.name != lesson_name):
                trans_lesson = get_lang_node(lesson_obj.id,lesson_language)
                if trans_lesson:
                    trans_lesson.name = lesson_name
                else:
                    lesson_obj.name = lesson_name
                # if lesson_language:
                #     language = get_language_tuple(lesson_language)
                #     lesson_obj.language = language
                lesson_obj.save(group_id=group_id)
                save_node_to_es(lesson_obj)
                unit_structure = get_unit_hierarchy(unit_group_obj, request.LANGUAGE_CODE)
                msg = u'Lesson name updated.'
                result_dict = {'success': 1, 'unit_hierarchy': unit_structure, 'msg': str(lesson_obj.id)}
            else:
                unit_structure = get_unit_hierarchy(unit_group_obj, request.LANGUAGE_CODE)
                msg = u'Nothing to update.'
                result_dict = {'success': 1, 'unit_hierarchy': unit_structure, 'msg': msg}

        else: # creating a fresh lesson object
            user_id = request.user.id
            new_lesson_obj = node_collection.collection.GSystem()
            new_lesson_obj.fill_gstystem_values(name=lesson_name,
                                            content=lesson_content,
                                            member_of=gst_lesson_id,
                                            group_set=unit_group_obj._id,
                                            created_by=user_id,
                                            status=u'PUBLISHED')
            # print new_lesson_obj
            if lesson_language:
                language = get_language_tuple(lesson_language)
                new_lesson_obj.language = language
            new_lesson_obj.save(groupid=group_id)
            save_node_to_es(new_lesson_obj)
            unit_group_obj.collection_set.append(new_lesson_obj._id)
            unit_group_obj.save(groupid=group_id)
            save_node_to_es(unit_group_obj)
            unit_structure = get_unit_hierarchy(unit_group_obj, request.LANGUAGE_CODE)

            msg = u'Added lesson under lesson: ' + unit_group_obj.name
            result_dict = {'success': 1, 'unit_hierarchy': unit_structure, 'msg': str(new_lesson_obj._id)}
            # return HttpResponse(json.dumps(unit_structure))

    # return HttpResponse(1)
    return HttpResponse(json.dumps(result_dict))

def create_grelation(subject_id, relation_type_node, right_subject_id_or_list, **kwargs):
    """Creates single or multiple GRelation documents (instances) based on given
    RelationType's cardinality (one-to-one / one-to-many).

    Arguments:
    subject_id -- ObjectId of the subject-node
    relation_type_node -- Document of the RelationType node (Embedded document)
    right_subject_id_or_list --
      - When one to one relationship: Single ObjectId of the right_subject node
      - When one to many relationship: List of ObjectId(s) of the right_subject node(s)

    Returns:
    - When one to one relationship: Created/Updated/Existed document.
    - When one to many relationship: Created/Updated/Existed list of documents.

    kwargs -- can hold the scope value
    """
    gr_node = None
    multi_relations = False
    triple_scope_val = kwargs.get('triple_scope', None)
    language = get_language_tuple(kwargs.get('language', None))
    '''
    Example:
    triple_scope:
      {
        relation_type_scope : {'alt_format': 'mp4', 'alt_size': '720p', 'alt_language': 'hi'},
        object_scope : unicode,
        subject_scope : unicode
      }

    In next phase, validate the scope values by adding:
        GSTUDIO_FORMAT_SCOPE_VALUES
        GSTUDIO_SIZE_SCOPE_VALUES
        GSTUDIO_LANGUAGE_SCOPE_VALUES
        in settings.py
        - katkamrachana, 23-12-2016
    '''
    try:
        subject_id = ObjectId(subject_id)

        def _create_grelation_node(subject_id, relation_type_node, right_subject_id_or_list, relation_type_text, triple_scope_val=None):
            # Code for creating GRelation node
            print("inside _create_grelation")
            gr_node = GRelation()
            print("gr_node",gr_node)
            gr_node.subject = ObjectId(subject_id)
            gr_node.relation_type = ObjectId(relation_type_node.id)
            gr_node.right_subject = ObjectId(right_subject_id_or_list)
            # gr_node.relation_type_scope = relation_type_scope
            gr_node.language = language
            gr_node.status = u"PUBLISHED"
            #print "post assiging:",gr_node
            gr_node.save()
            #print "saved"
            save_triple_to_es(gr_node)
            # gr_node.save(triple_node=relation_type_node, triple_id=relation_type_node._id)

            gr_node_name = gr_node.name
            #print "post save:",gr_node_name
            info_message = "%(relation_type_text)s: GRelation (%(gr_node_name)s) " % locals() \
                + "created successfully.\n"

            relation_type_node_name = relation_type_node.name
            relation_type_node_inverse_name = relation_type_node.inverse_name

            # left_subject = node_collection.one({
            #     "_id": subject_id,
            #     "relation_set." + relation_type_node_name: {"$exists": True}
            # })
            #print "post saving"
            q = Q('bool',must = [Q('match',id = str(subject_id)),Q('exists',field = "relation_set." + relation_type_node_name)])
            s1 = Search(using=es, index='nodes',doc_type="node").query(q)
            left_subject = s1.execute()
        
            if triple_scope_val:
                gr_node = update_scope_of_triple(gr_node,relation_type_node, triple_scope_val, is_grel=True)

            if s1.count() > 0:
                                # Update value of grelation in existing as key-value pair value in
                                # given node's "relation_set" field
                # node_collection.collection.update({
                #     "_id": subject_id,
                #     "relation_set." + relation_type_node_name: {'$exists': True}
                # }, {
                #     "$addToSet": {"relation_set.$." + relation_type_node_name: right_subject_id_or_list}
                # },
                #     upsert=False, multi=False
                # )
                #print "in if of left subject"
                q = Q('bool',must = [Q('match',id = str(subject_id)),Q('exists',field = "relation_set." + relation_type_node_name)])
                f1 = "relation_set." + relation_type_node_name
                s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.add(params.val)", lang="painless",params={'val':str(right_subject_id_or_list)})
                s2 = s1.execute()
                # left_subject = s2[0]


            else:
                #print "in else of left subject"
                # Add grelation as new key-value pair value in given node's
                # relation_set field
                # node_collection.collection.update({
                #     "_id": subject_id
                # }, {
                #     "$addToSet": {"relation_set": {relation_type_node_name: [right_subject_id_or_list]}}
                # },
                #     upsert=False, multi=False
                # )

                q = Q('bool',must = [Q('match',id = str(subject_id))])
                s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.relation_set.add(params.val)", lang="painless",params={'val':{relation_type_node_name:[str(right_subject_id_or_list)]}})
                s2 = s1.execute()

            # right_subject = node_collection.one({
            #     '_id': right_subject_id_or_list,
            #     "relation_set." + relation_type_node_inverse_name: {"$exists": True}
            # }, {
            #     'relation_set': 1
            # })
            
            q = Q('bool',must = [Q('match',id = str(right_subject_id_or_list)),Q('exists',field = "relation_set." + relation_type_node_inverse_name)])
            s1 = Search(using=es, index='nodes',doc_type="node").query(q)
            right_subject = s1.execute()
    
            
            if s1.count() > 0:
                # Update value of grelation in existing as key-value pair value in
                # given node's "relation_set" field
                # node_collection.collection.update({
                #     "_id": right_subject_id_or_list, "relation_set." + relation_type_node_inverse_name: {'$exists': True}
                # }, {
                #     "$addToSet": {"relation_set.$." + relation_type_node_inverse_name: subject_id}
                # },
                #     upsert=False, multi=False
                # )
                #print "inside right_subject if loop inside the create_gattribute"
                q = Q('bool',must = [Q('match',id = str(right_subject_id_or_list)),Q('exists',field = "relation_set." + relation_type_node_inverse_name)])
                f1 = "relation_set." + relation_type_node_inverse_name
                s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.add(params.val)", lang="painless",params={'val':str(subject_id)})
                #print "query",q
                s2 = s1.execute()

            else:
                # Add grelation as new key-value pair value in given node's
                # relation_set field
                # node_collection.collection.update({
                #     "_id": right_subject_id_or_list
                # }, {
                #     "$addToSet": {"relation_set": {relation_type_node_inverse_name: [subject_id]}}
                # },
                #     upsert=False, multi=False
                # )
                #print "in else of right subject"
                q = Q('bool',must = [Q('match',id = str(right_subject_id_or_list))])
                s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.relation_set.add(params.val)", lang="painless",params={'val':{relation_type_node_inverse_name:str(subject_id)}})
                s2 = s1.execute()

            return gr_node

        def _update_deleted_to_published(gr_node, relation_type_node, relation_type_text, triple_scope_val=None):
            gr_node.status = u"PUBLISHED"
            # gr_node.language = language
            gr_node.save()
            # gr_node.save(triple_node=relation_type_node, triple_id=relation_type_node._id)
            save_triple_to_es(gr_node)
            gr_node_name = gr_node.name
            relation_type_node_name = relation_type_node.name
            relation_type_node_inverse_name = relation_type_node.inverse_name

            subject_id = gr_node.subject
            right_subject = gr_node.right_subject

            info_message = " %(relation_type_text)s: GRelation (%(gr_node_name)s) " % locals() \
                + \
                "status updated from 'DELETED' to 'PUBLISHED' successfully.\n"

            # node_collection.collection.update({
            #     "_id": subject_id, "relation_set." + relation_type_node_name: {'$exists': True}
            # }, {
            #     "$addToSet": {"relation_set.$." + relation_type_node_name: right_subject}
            # },
            #     upsert=False, multi=False
            # )

            q = Q('bool',must = [Q('match',id = subject_id),Q('exists',field = "relation_set." + relation_type_node_name)])
            f1 = "relation_set." + relation_type_node_name
            s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.add(params.val)", lang="painless",params={'val':right_subject})
            s2 = s1.execute()


            # node_collection.collection.update({
            #     "_id": right_subject, "relation_set." + relation_type_node_inverse_name: {'$exists': True}
            # }, {
            #     "$addToSet": {'relation_set.$.' + relation_type_node_inverse_name: subject_id}
            # },
            #     upsert=False, multi=False
            # )


            q = Q('bool',must = [Q('match',id = subject_id),Q('exists',field = "relation_set." + relation_type_node_inverse_name)])
            f1 = "relation_set." + relation_type_node_inverse_name
            s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.add(params.val)", lang="painless",params={'val':subject_id})
            s2 = s1.execute()

            return gr_node


        if relation_type_node["object_cardinality"]:
            # If object_cardinality value exists and greater than 1 (or eaqual to 100)
            # Then it signifies it's a one to many type of relationship
            # assign multi_relations = True
            type_of_relationship = member_of_names_list(relation_type_node)
            if relation_type_node["object_cardinality"] > 1:
                multi_relations = True

                if META_TYPE[3] in type_of_relationship:
                    # If Binary relationship found

                    # Check whether right_subject_id_or_list is list or not
                    # If not convert it to list
                    if not isinstance(right_subject_id_or_list, list):
                        right_subject_id_or_list = [right_subject_id_or_list]

                    # Check whether all values of a list are of ObjectId data-type or not
                    # If not convert them to ObjectId
                    for i, each in enumerate(right_subject_id_or_list):
                        right_subject_id_or_list[i] = ObjectId(each)

                else:
                    # Relationship Other than Binary one found; e.g, Triadic
                    if right_subject_id_or_list:
                        if not isinstance(right_subject_id_or_list[0], list):
                            right_subject_id_or_list = [
                                right_subject_id_or_list]

                        # right_subject_id_or_list: [[id, id, ...], [id, id,
                        # ...], ...]
                        for i, each_list in enumerate(right_subject_id_or_list):
                            # each_list: [id, id, ...]
                            for j, each in enumerate(each_list):
                                right_subject_id_or_list[i][j] = ObjectId(each)

            else:
                if META_TYPE[3] in type_of_relationship:
                    # If Binary relationship found
                    if isinstance(right_subject_id_or_list, list):
                        right_subject_id_or_list = ObjectId(
                            right_subject_id_or_list[0])

                    else:
                        right_subject_id_or_list = ObjectId(
                            right_subject_id_or_list)
                else:
                    # Relationship Other than Binary one found; e.g, Triadic
                    # right_subject_id_or_list: [[id, id, ...], [id, id, ...],
                    # ...]
                    if isinstance(right_subject_id_or_list, ObjectId):
                        right_subject_id_or_list = [right_subject_id_or_list]
                    if right_subject_id_or_list:
                        if isinstance(right_subject_id_or_list[0], list):
                            # Reduce it to [id, id, id, ...]
                            right_subject_id_or_list = right_subject_id_or_list[
                                0]

                        for i, each_id in enumerate(right_subject_id_or_list):
                            right_subject_id_or_list[i] = ObjectId(each_id)

        if multi_relations:
            # For dealing with multiple relations (one to many)

            # # Iterate and find all relationships (including DELETED ones' also)
            # nodes = triple_collection.find({
            #     '_type': "GRelation", 'subject': subject_id,
            #     'relation_type': relation_type_node._id
            # })

            q = Q('bool',must = [Q('match',type = 'GRelation'),Q('match',subject=str(subject_id)),Q('match', relation_type = relation_type_node.id )])
            # f1 = "relation_set." + relation_type_node_inverse_name
            s1 = Search(using=es, index='triples',doc_type="triple").query(q)
            nodes = s1.execute()

            gr_node_list = []

            for n in nodes:
                if n.right_subject in right_subject_id_or_list:
                    if n.status != u"DELETED":
                        # If match found with existing one's, then only remove that ObjectId from the given list of ObjectIds
                        # Just to remove already existing entries (whose status
                        # is PUBLISHED)
                        right_subject_id_or_list.remove(n.right_subject)
                        gr_node_list.append(n)
                        # if triple_scope_val:
                        #     n = update_scope_of_triple(n, relation_type_node, triple_scope_val, is_grel=True)

                        # node_collection.collection.update(
                        #     {'_id': subject_id, 'relation_set.' +
                        #         relation_type_node.name: {'$exists': True}},
                        #     {'$addToSet': {
                        #         'relation_set.$.' + relation_type_node.name: n.right_subject}},
                        #     upsert=False, multi=False
                        # )

                        q = Q('bool',must = [Q('match',id = str(subject_id)),Q('exists',field = "relation_set." + relation_type_node.name)])
                        f1 = "relation_set." + relation_type_node.name
                        s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.add(params.val)", lang="painless",params={'val':n.right_subject})
                        s2 = s1.execute()

                        # node_collection.collection.update(
                        #     {'_id': n.right_subject, 'relation_set.' +
                        #         relation_type_node.inverse_name: {'$exists': True}},
                        #     {'$addToSet': {
                        #         'relation_set.$.' + relation_type_node.inverse_name: subject_id}},
                        #     upsert=False, multi=False
                        # )

                        q = Q('bool',must = [Q('match',id = n.right_subject),Q('exists',field = "relation_set." + relation_type_node.inverse_name)])
                        f1 = "relation_set." + relation_type_node.inverse_name
                        s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.add(params.val)", lang="painless",params={'val':subject_id})
                        s2 = s1.execute()

                        #n.reload()

                else:
                    # Case: When already existing entry doesn't exists in newly come list of right_subject(s)
                    # So change their status from PUBLISHED to DELETED
                    n.status = u"DELETED"
                    n.save()
                    save_node_to_es(n)
                    # n.save(triple_node=relation_type_node, triple_id=relation_type_node._id)

                    info_message = " MultipleGRelation: GRelation (" + n.name + \
                        ") status updated from 'PUBLISHED' to 'DELETED' successfully.\n"

                    # node_collection.collection.update({
                    #     '_id': subject_id, 'relation_set.' + relation_type_node.name: {'$exists': True}
                    # }, {
                    #     '$pull': {'relation_set.$.' + relation_type_node.name: n.right_subject}
                    # },
                    #     upsert=False, multi=False
                    # )

                    q = Q('bool',must = [Q('match',id = subject_id),Q('exists',field = "relation_set." + relation_type_node.name)])
                    f1 = "relation_set." + relation_type_node.name
                    s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.remove(params.val)", lang="painless",params={'val':n.right_subject})
                    s2 = s1.execute()

                    # res = node_collection.collection.update({
                    #     '_id': n.right_subject, 'relation_set.' + relation_type_node.inverse_name: {'$exists': True}
                    # }, {
                    #     '$pull': {'relation_set.$.' + relation_type_node.inverse_name: subject_id}
                    # },
                    #     upsert=False, multi=False
                    # )

                    q = Q('bool',must = [Q('match',id = n.right_subject),Q('exists',field = "relation_set." + relation_type_node.inverse_name)])
                    f1 = "relation_set." + relation_type_node.inverse_name
                    s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.remove(params.val)", lang="painless",params={'val':subject_id})
                    s2 = s1.execute()

            if right_subject_id_or_list:
                #print "right subject list",right_subject_id_or_list
                # If still ObjectId list persists, it means either they are new ones'
                # or from deleted ones'
                # For deleted one's, find them and modify their status to PUBLISHED
                # For newer one's, create them as new document
                for nid in right_subject_id_or_list:
                    #print "each from list:",nid
                    # gr_node = triple_collection.one({
                    #     '_type': "GRelation", 'subject': subject_id,
                    #     'relation_type': relation_type_node._id, 'right_subject': nid
                    # })

                    q = Q('bool',must = [Q('match',type = 'GRelation'),Q('match',subject = str(subject_id)),Q('match', relation_type = relation_type_node.id),Q('match', right_subject = str(nid))])
                    # f1 = "relation_set." + relation_type_node_name
                    s1 = Search(using=es, index='triples',doc_type="triple").query(q)
                    gr_node = s1.execute()
                    

                    if s1.count() == 0:
                        # New one found so create it
                        # check for relation_type_scope variable in kwargs and pass
                        gr_node = _create_grelation_node(
                            subject_id, relation_type_node, nid, "MultipleGRelation", triple_scope_val)
                        gr_node_list.append(gr_node)

                    else:
                        # Deleted one found so change it's status back to
                        # Published
                        if gr_node.status == u'DELETED':
                            gr_node = _update_deleted_to_published(
                                gr_node, relation_type_node, "MultipleGRelation")
                            gr_node_list.append(gr_node)

                        else:
                            error_message = " MultipleGRelation: Corrupt value found - GRelation (" + \
                                gr_node.name + ")!!!\n"
                            # raise Exception(error_message)

            return gr_node_list

        else:
            # For dealing with single relation (one to one)
            gr_node = None

            relation_type_node_id = relation_type_node.id
            relation_type_node_name = relation_type_node.name
            relation_type_node_inverse_name = relation_type_node.inverse_name
            #print "in final else to create node:",relation_type_node.name
            # gr_node_cur = triple_collection.find({
            #     "_type": "GRelation", "subject": subject_id,
            #     "relation_type": relation_type_node_id
            # })

            q = Q('bool',must = [Q('match',type = 'GRelation'),Q('match',subject = str(subject_id)),Q('match', right_subject = relation_type_node_id)])
            # f1 = "relation_set." + relation_type_node_name
            s1 = Search(using=es, index='triples',doc_type="triple").query(q)
            gr_node_cur = s1.execute()

            for node in gr_node_cur:
                node_name = node.name
                node_status = node.status
                node_right_subject = node.right_subject

                if node_right_subject == right_subject_id_or_list:
                    # If match found, it means it could be either DELETED one
                    # or PUBLISHED one

                    if node_status == u"DELETED":
                        # If deleted, change it's status back to Published from
                        # Deleted
                        node = _update_deleted_to_published(
                            node, relation_type_node, "SingleGRelation", triple_scope_val)

                    elif node_status == u"PUBLISHED":
                        if triple_scope_val:
                            node = update_scope_of_triple(node, relation_type_node, triple_scope_val, is_grel=True)

                        #node_collection.collection.update({
                        #    "_id": subject_id, "relation_set." + relation_type_node_name: {'$exists': True}
                        #}, {
                        #    "$addToSet": {"relation_set.$." + relation_type_node_name: node_right_subject}
                        #},
                        #    upsert=False, multi=False
                        #)

                        q = Q('bool',must = [Q('match',id = subject_id),Q('exists',field = "relation_set." + relation_type_node_name)])
                        f1 = "relation_set." + relation_type_node_name
                        s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.add(params.val)", lang="painless",params={'val':node_right_subject})
                        s2 = s1.execute()

                        # node_collection.collection.update({
                        #     "_id": node_right_subject, "relation_set." + relation_type_node_inverse_name: {'$exists': True}
                        # }, {
                        #     "$addToSet": {"relation_set.$." + relation_type_node_inverse_name: subject_id}
                        # },
                        #     upsert=False, multi=False
                        # )

                        q = Q('bool',must = [Q('match',id = node_right_subject),Q('exists',field = "relation_set." + relation_type_node_inverse_name)])
                        f1 = "relation_set." + relation_type_node_inverse_name
                        s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.add(params.val)", lang="painless",params={'val':subject_id})
                        s2 = s1.execute()


                        info_message = " SingleGRelation: GRelation (%(node_name)s) already exists !\n" % locals(
                        )

                    # Set gr_node value as matched value, so that no need to
                    # create new one
                    node.reload()
                    gr_node = node

                else:
                    # If match not found and if it's PUBLISHED one, modify it
                    # to DELETED
                    if node.status == u'PUBLISHED':
                        node.status = u"DELETED"
                        node.save()
                        save_triple_to_es(node)
                        # node.save(triple_node=relation_type_node, triple_id=relation_type_node._id)

                        #node_collection.collection.update({
                        #    '_id': subject_id, 'relation_set.' + relation_type_node_name: {'$exists': True}
                        #}, {
                        #    '$pull': {'relation_set.$.' + relation_type_node_name: node_right_subject}
                        #},
                        #    upsert=False, multi=False
                        #)

                        q = Q('bool',must = [Q('match',id = subject_id),Q('exists',field = "relation_set." + relation_type_node_name)])
                        f1 = "relation_set." + relation_type_node_name
                        s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.remove(params.val)", lang="painless",params={'val':node_right_subject})
                        s2 = s1.execute()


                        # node_collection.collection.update({
                        #     '_id': node_right_subject, 'relation_set.' + relation_type_node_inverse_name: {'$exists': True}
                        # }, {
                        #     '$pull': {'relation_set.$.' + relation_type_node_inverse_name: subject_id}
                        # },
                        #     upsert=False, multi=False
                        # )

                        q = Q('bool',must = [Q('match',id = node_right_subject),Q('exists',field = "relation_set." + relation_type_node_inverse_name)])
                        f1 = "relation_set." + relation_type_node_inverse_name
                        s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.add(params.val)", lang="painless",params={'val':str(subject_id)})
                        s2 = s1.execute()


                        info_message = " SingleGRelation: GRelation (%(node_name)s) status " % locals() \
                            + \
                            "updated from 'PUBLISHED' to 'DELETED' successfully.\n"

            if gr_node is None:
                # Code for creation
                #print "inside if",subject_id, relation_type_node, right_subject_id_or_list, "SingleGRelation", triple_scope_val
                gr_node = _create_grelation_node(subject_id, relation_type_node, right_subject_id_or_list, "SingleGRelation")

            return gr_node

    except Exception as e:
        error_message = "\n GRelationError (line #" + \
            str(exc_info()[-1].tb_lineno) + "): " + str(e) + "\n"
        raise Exception(error_message)

def create_gattribute(subject_id, attribute_type_node, object_value=None, **kwargs):

    def _update_attr_set(attr_set_list_of_dicts, attr_key, attr_value):
        temp_attr_dict = get_dict_from_list_of_dicts(attr_set_list_of_dicts)
        temp_attr_dict.update({unicode(attr_key): attr_value})
        return [{k:v} for k, v in temp_attr_dict.iteritems()]

    ga_node = None
    info_message = ""
    old_object_value = None
    triple_scope_val = kwargs.get('triple_scope', None)
    
    q = Q('bool',must = [Q('match',type = 'GAttribute'),Q('match',subject= subject_id),Q('match',attribute_type= attribute_type_node.id)])
    # f1 = "relation_set." + relation_type_node_name                                                                                                            
    s1 = Search(using=es, index='triples',doc_type="triple").query(q)
    ga_node = s1.execute()
    
    '''
    Example:
    triple_scope:
      {
        attribute_type_scope : {'alt_format': 'mp4', 'alt_size': '720p', 'alt_language': 'hi'},
        object_scope : unicode,
        subject_scope : unicode
      }

    '''
    if s1.count() == 0:
        # Code for creation
        try:
            ga_node = GAttribute()

            ga_node.subject = ObjectId(subject_id)
            ga_node.attribute_type = ObjectId(attribute_type_node.id)

            if (not object_value) and type(object_value) != bool:
                # this is when value of attribute is cleared/empty
                # in this case attribute will be created with status deleted
                object_value = u"None"
                ga_node.status = u"DELETED"

            else:
                ga_node.status = u"PUBLISHED"

            ga_node.object_value = object_value
            
            # ga_node.save(triple_node=attribute_type_node, triple_id=attribute_type_node._id)
            ga_node.save()
            
            print("post saving",ga_node.reload())

            if triple_scope_val:
                ga_node = update_scope_of_triple(ga_node,attribute_type_node, triple_scope_val, is_grel=False)
            save_triple_to_es(ga_node)
            
            if ga_node.status == u"DELETED":
                info_message = " GAttribute (" + ga_node.name + \
                    ") created successfully with status as 'DELETED'!\n"

            else:
                info_message = " GAttribute (" + \
                    ga_node.name + ") created successfully.\n"

                # Fetch corresponding document & append into it's attribute_set
                #node_collection.collection.update({'_id': subject_id},
                #                                  {'$addToSet': {
                #                                      'attribute_set': {attribute_type_node.name: object_value}}},
                #                                  upsert=False, multi=False
                #                                  )
                q = Q('bool',must = [Q('match',id = str(subject_id))])
                #f1 = "relation_set." + relation_type_node_name
                s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.attribute_set.add(params.val)", lang="painless",params={'val':{attribute_type_node.name: object_value}})
                s2 = s1.execute()
            is_ga_node_changed = True

        except Exception as e:
            error_message = "\n GAttributeCreateError: " + str(e) + "\n"
            raise Exception(error_message)

    else:
        # Code for updating existing gattribute
        is_ga_node_changed = False
        print("ga node changd",is_ga_node_changed)
        try:
            if (not object_value) and type(object_value) != bool:
                # this is when value of attribute is cleared/empty
                # in this case attribute will be set with status deleted
                old_object_value = ga_node.object_value

                ga_node.status = u"DELETED"
                ga_node.save()
                # ga_node.save(triple_node=attribute_type_node, triple_id=attribute_type_node._id)
                if triple_scope_val:
                    ga_node = update_scope_of_triple(ga_node,attribute_type_node, triple_scope_val, is_grel=False)
                save_triple_to_es(ga_node)
                info_message = " GAttribute (" + ga_node.name + \
                    ") status updated from 'PUBLISHED' to 'DELETED' successfully.\n"

                # Fetch corresponding document & update it's attribute_set with
                # proper value
                #node_collection.collection.update({'_id': subject_id, 'attribute_set.' + attribute_type_node.name: old_object_value}, {'$pull': {'attribute_set': {attribute_type_node.name: old_object_value}}}, upsert=False, multi=False)

                f1 = 'attribute_set.'+ attribute_type_node.name
                q = Q('bool',must = [Q('match',id= subject_id),Q('match',f1 = old_object_value)])
                s1 = UpdateByQuery(using=es, index='nodes',doc_type="node").query(q).script(source="ctx._source.f1.add(params.val)", lang="painless",params={'val':{attribute_type_node.name: old_object_value}})
                s2 = s1.execute()
            else:
                print("inside else")
                if type(ga_node.object_value) == list:
                    #print "inside list condtn"
                    if type(ga_node.object_value[0]) == dict:
                        old_object_value = ga_node.object_value

                        if len(old_object_value) != len(object_value):
                            ga_node.object_value = object_value
                            #print "changing the ga node changed"
                            is_ga_node_changed = True

                        else:
                            #print "Old value and new value:",old_object_value,'\n',object_value
                            pairs = zip(old_object_value, object_value)
                            #print "pairs:",pairs
                            if any(x != y for x, y in pairs):
                                #print "change ga node in else"
                                ga_node.object_value = object_value
                                is_ga_node_changed = True

                    elif type(ga_node.object_value[0]) == list:
                        if ga_node.object_value != object_value:
                            old_object_value = ga_node.object_value
                            ga_node.object_value = object_value
                            is_ga_node_changed = True

                    else:
                        if set(ga_node.object_value) != set(object_value):
                            old_object_value = ga_node.object_value
                            ga_node.object_value = object_value
                            is_ga_node_changed = True

                elif type(ga_node.object_value) == dict:
                    if cmp(ga_node.object_value, object_value) != 0:
                        old_object_value = ga_node.object_value
                        ga_node.object_value = object_value
                        is_ga_node_changed = True

                else:
                    if ga_node.object_value != object_value:
                        old_object_value = ga_node.object_value
                        ga_node.object_value = object_value
                        is_ga_node_changed = True

                if is_ga_node_changed or ga_node.status == u"DELETED":
                    if ga_node.status == u"DELETED":
                        ga_node.status = u"PUBLISHED"
                        ga_node.save()
                        save_triple_to_es(ga_node)
                        # ga_node.save(triple_node=attribute_type_node, triple_id=attribute_type_node._id)
                        if triple_scope_val:
                            ga_node = update_scope_of_triple(ga_node,attribute_type_node, triple_scope_val, is_grel=False)

                        info_message = " GAttribute (" + ga_node.name + \
                            ") status updated from 'DELETED' to 'PUBLISHED' successfully.\n"

                        # Fetch corresponding document & append into it's
                        # attribute_set
                        # node_collection.collection.update({'_id': subject_id},
                        #                                   {'$addToSet': {
                        #                                       'attribute_set': {attribute_type_node.name: object_value}}},
                        #                                   upsert=False, multi=False)
                        subject_node_obj = get_node_by_id(subject_id)
                        subject_node_obj.attribute_set = _update_attr_set(
                                                            subject_node_obj.attribute_set,
                                                            attribute_type_node.name,
                                                            object_value
                                                        )
                        save_node_to_es(subject_node_obj)


                    else:
                        ga_node.status = u"PUBLISHED"
                        ga_node.save()
                        save_triple_to_es(ga_node)
                        # ga_node.save(triple_node=attribute_type_node, triple_id=attribute_type_node._id)
                        if triple_scope_val:
                            ga_node = update_scope_of_triple(ga_node,attribute_type_node, triple_scope_val, is_grel=False)

                        info_message = " GAttribute (" + \
                            ga_node.name + ") updated successfully.\n"

                        # Fetch corresponding document & update it's
                        # attribute_set with proper value
                        # node_collection.collection.update({'_id': subject_id, 'attribute_set.' + attribute_type_node.name: {"$exists": True}},
                        #                               {'$set': {
                        #                                   'attribute_set.$.' + attribute_type_node.name: ga_node.object_value}},
                        #                               upsert=False, multi=False)
                        subject_node_obj = get_node_by_id(subject_id)
                        subject_node_obj.attribute_set = _update_attr_set(
                                                            subject_node_obj.attribute_set,
                                                            attribute_type_node.name,
                                                            ga_node.object_value
                                                        )
                        save_node_to_es(subject_node_obj)
                else:
                    info_message = " GAttribute (" + ga_node.name + \
                        ") already exists (Nothing updated) !\n"

        except Exception as e:
            error_message = "\n GAttributeUpdateError: " + str(e) + "\n"
            raise Exception(error_message)

    if "is_changed" in kwargs:
        ga_dict = {}
        ga_dict["is_changed"] = is_ga_node_changed
        ga_dict["node"] = ga_node
        ga_dict["before_obj_value"] = old_object_value
        return ga_dict
    else:
        return ga_node


def get_group_resources(request, group_id, res_type="Page"):
    #print "in es_queries get_group_resources"
    except_collection_set = []
    res_cur = None
    template = "ndf/group_pages.html"
    card_class = 'activity-page'

    try:
        # res_query = {'_type': 'GSystem', 'group_set': ObjectId(group_id)}
        # q1 = Q('bool',must = [])
        except_collection_set_of_id = request.GET.get('except_collection_set_of_id', None)
        #print "except_collection_set_of_id:",except_collection_set_of_id
        except_collection_set_of_obj = get_node_by_id(except_collection_set_of_id)
        #print "except_collection_set_of_obj:",except_collection_set_of_obj.collection_set
        if except_collection_set_of_obj:
            except_collection_set = except_collection_set_of_obj.collection_set
        #     if except_collection_set:
        #         # res_query.update({'_id': {'$nin': except_collection_set}})
        #         q2 = Q('match',id = str(except_collection_set))
        if res_type.lower() == "page":
            gst_page_name, gst_page_id = get_gst_name_id('Page')
            gst_blog_type_name, gst_blog_type_id = get_gst_name_id("Blog page")
            gst_info_type_name, gst_info_type_id = get_gst_name_id("Info page")
            # res_query.update({'type_of': {'$nin': [gst_blog_type_id, gst_info_type_id]}})
            # res_query.update({'member_of': gst_page_id})

        q = Q('bool',must = [Q('match',type = 'GSystem'),Q('match',group_set = str(group_id)),Q('match',member_of = str(gst_page_id))],must_not= [Q('terms',type_of = [str(gst_blog_type_id), str(gst_info_type_id)])])
        #print "get_group_resources:",q
        s1 = Search(using=es, index='nodes',doc_type="node").query(q)
        res_cur = s1.execute()
        #print "res_cur:",res_cur
        # right_subject = s2[0]
        # res_cur = node_collection.find(res_query).sort('last_update', -1)

    except Exception as get_group_resources_err:
      print("\n Error occurred. Error: {0}".format(str(get_group_resources_err)))
      pass

    variable = RequestContext(request, {'cursor': res_cur, 'groupid': group_id, 'group_id': group_id, 'card_class': card_class })
    return render_to_response(template, variable)
