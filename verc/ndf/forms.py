import datetime

from django import forms
#from django_mongokit.forms import DocumentForm
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

from .models import User
'''
from django_registration.forms import RegistrationForm
#from passwords.fields import PasswordField

class UserRegistrationForm(RegistrationForm):
    #password1 = PasswordField(label="Password")
    class Meta(RegistrationForm.Meta):
        model = User

class UserChangeform(PasswordChangeForm):
    new_password1 = PasswordField(label="New password") 

class UserResetform(SetPasswordForm):
    new_password1 = PasswordField(label="New password")
'''
