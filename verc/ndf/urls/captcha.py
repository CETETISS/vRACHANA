from django.conf.urls import  url

from ndf.views.captcha import *

urlpatterns = [
    url(r'^validate_captcha/', captcha_validate, name='captcha_validate'),
    url(r'^new_captcha/', new_captcha, name='new_captcha')
    ]
