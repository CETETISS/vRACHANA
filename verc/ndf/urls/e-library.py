from django.conf.urls import  url
from ndf.views.e_library import *
urlpatterns = [
					   url(r'^/?$', resource_list, name="e-library"),
                                            url(r'^/domain-wise$', resource_list_domainwise, name="e-library_domainwise"),
                       url(r'^/(?P<app_id>[\w-]+)$', resource_list, name='resource_list'),
                       #url(r'^/details/(?P<_id>[\w-]+)$', file_detail, name='resource_detail'),
                       url(r'^/(?P<filetype>[\w-]+)/page-no=(?P<page_no>\d+)/$', elib_paged_file_objs, name='elib_paged_file_objs')
]
