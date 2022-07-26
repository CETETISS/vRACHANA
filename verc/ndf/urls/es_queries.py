from django.conf.urls import patterns, url
print "in es_queries urls"
urlpatterns = patterns('ndf.views.es_queries',
                        url(r'(^?P<group_id>[^/]+)/module/(?P<node_id>[\w-]+)/(?P<title>[^/]+)/?$', 'module_detail', name='module_detail'),
                        url(r'^/save_course_page/$', 'save_course_page', name='save_course_page'),
                        #url(r'(^?P<group_id>[^/]+)/course/content/$', 'course_content', name='course_content'),
                       )
