from django.conf import settings
from django.conf.urls import include, url

from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.static import serve

from ndf.views.ajax_views import register
from verc.settings import GSTUDIO_SITE_NAME, GSTUDIO_OER_GROUPS

urlpatterns = [
                        #url(r'^accounts/login/', include('captcha.urls')),
                        url(r'^account/register/', register, name='custom_register'), 
              ]