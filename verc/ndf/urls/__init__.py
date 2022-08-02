from django.conf import settings
from django.conf.urls import include, url
#from django.contrib.auth import get_user_model
#User = get_user_model()
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.static import serve

from ndf.forms import *
from verc.settings import GSTUDIO_SITE_NAME, GSTUDIO_OER_GROUPS
from ndf.views.home import homepage, landing_page

login_template = 'login.html'
#logout_template = "landidjango.template.exceptidjango.template.exceptidjango.template.exceptions.TemplateDoesNotExist: registration/login.htmlons.TemplateDoesNotExist: registration/login.htmlons.TemplateDoesNotExist: registration/login.htmlng_page_clix_oer.html"

if settings.DEBUG:
      urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
]
      
#from ndf.views.es_queries import *
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib import admin
urlpatterns += [
                        #url(r'^captcha/', include('captcha.urls')),
                        #url(r'^', include('ndf.urls.captcha')), 
                        url(r'^$', homepage, {"group_id": "home"}, name="homepage"),
                        #url(r'^$', homepage, {"group_id": "home"}, name="homepage"),
                        #url(r'^test-delete/$', test_delete, name='test_delete'),
                        #url(r'^test-session/$', test_session, name='test_session'),
                        url(r'^i18n/', include('django.conf.urls.i18n')),
                        #url(r'^status/cache/$', cache_status),
                        # gstudio admin url's
                        url(r'^admin/', admin.site.urls),
                        url('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('ndf/images/favicon/favicon.ico'))),

                        #ajax URLS
                        url(r'^/ajax/', include('ndf.urls.ajax_urls')),
                        url('accounts/', include('django.contrib.auth.urls')),
                        #url(r'^(?P<groupid>[^/]+)/e-library', include('ndf.urls.e-library')),
                        #url(r'^(?P<group_id>[^/]+)/?$', homepage, name="homepage1"),
                        
]
