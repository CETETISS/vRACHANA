from django.contrib import admin
from django.conf.urls import include, url

admin.autodiscover()

urlpatterns = [
    #(r'^data[\/]?', include('gnowsys_ndf.ndf.urls.adminDashboard')),
    #(r'^designer[\/]?', include('gnowsys_ndf.ndf.urls.adminDesignerDashboard')),

    # django's admin site url's
    url(r'^',admin.site.urls),

    # moved to urls.dev_utils.py
    # url(r'^query-doc/(?P<doc_id_or_name>[^/]+)?$', 'gnowsys_ndf.ndf.views.dev_utils.query_doc'),
    # url(r'^query-doc/(?P<doc_id_or_name>[\w-]+)/(?P<option>[^/]+)?$', 'gnowsys_ndf.ndf.views.dev_utils.query_doc'),
]
