#------------------------------------------ Changing the website instances(Logo and database etc) -------------------------------------------------                    
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "*"]

import os

# Authentication related and Error reporting emails                                                                                                                    
# EMAIL_USE_TLS = ""                                                                                                                                                   
# ACCOUNT_ACTIVATION_DAYS = 2                                                                                                                                          
# #EMAIL_HOST = 'localhost'                                                                                                                                            
# EMAIL_HOST = 'localhost'                                                                                                                                             
# #DEFAULT_FROM_EMAIL = 'webmaster@clix.ss.org'                                                                                                                        
# DEFAULT_FROM_EMAIL = 'gdswetha@gmail.com'                                                                                                                            
# LOGIN_REDIRECT_URL = '/'                                                                                                                                             
# EMAIL_SUBJECT_PREFIX='[clix-ss-error-reporting]'                                                                                                                     
# SERVER_EMAIL = DEFAULT_FROM_EMAIL                                                                                                                                    
# EMAIL_PORT = ""                                                                                                                                                      
# ADMINS = (                                                                                                                                                           
#     "mrunal4888@gmail.com"                                                                                                                                           
# )                                                                                                                                                                    
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'                                                                                                        


ACCOUNT_ACTIVATION_DAYS = 2
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 25
EMAIL_HOST_USER = 'clix_admin@clixindia.org'
EMAIL_HOST_PASSWORD = 'cete@77ck'                                                                                                                                     
