from django.conf import settings
from django.conf.urls import include, url
#from django.contrib.auth import get_user_model
#User = get_user_model()
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.static import serve

#from ndf.forms import UserRegistrationForm

# from django.views.generic import RedirectView
#from django_registration.views import RegistrationView
#from django_registration.views import ActivationView
#from jsonrpc import jsonrpc_site
#from ve.ndf.views.cache import cache_status
# from gnowsys_ndf.ndf.forms import *
from verc.settings import GSTUDIO_SITE_NAME, GSTUDIO_OER_GROUPS
#from gnowsys_ndf.ndf.views.email_registration import password_reset_email, password_reset_error, GstudioEmailRegistrationForm
#from gnowsys_ndf.ndf.forms import UserChangeform, UserResetform
#from gnowsys_ndf.ndf.views.home import homepage, landing_page
#from gnowsys_ndf.ndf.views.methods import tag_info
#from gnowsys_ndf.ndf.views.custom_app_view import custom_app_view, custom_app_new_view
#from gnowsys_ndf.ndf.views import rpc_resources

#from gnowsys_ndf.ndf.views import rpc_resources

if GSTUDIO_SITE_NAME.lower() == 'verc':
    print("assigned templates")
    login_template = 'registration/login_clix.html'
    logout_template = "ndf/landing_page_clix_oer.html"
else:
    login_template = 'registration/login.html'
    logout_template = 'registration/logout.html'

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
                        #url(r'^$', homepage, {"group_id": "home"}, name="homepage"),
                        #url(r'^$', homepage, {"group_id": "home"}, name="homepage"),
                        #url(r'^test-delete/$', test_delete, name='test_delete'),
                        #url(r'^test-session/$', test_session, name='test_session'),
                        url(r'^i18n/', include('django.conf.urls.i18n')),
                        #url(r'^status/cache/$', cache_status),
                        # gstudio admin url's
                        url(r'^admin/', admin.site.urls),
                        url('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('ndf/images/favicon/favicon.ico'))),
                        #url(r'^accounts/', include('django_registration.backends.activation.urls')),
                        url(r'^accounts/', include('django.contrib.auth.urls')),
                        #url(r'^(?P<groupid>[^/]+)/e-library', include('ndf.urls.e-library')),
                        #url(r'^(?P<group_id>[^/]+)/?$', homepage, name="homepage1"),
                        
]
