from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from .managers import UserCustomManager


class User(AbstractUser):
    fullname = models.CharField(max_length=100)
    #username = StringField(_('username'),unique=True)
    #email = models.EmailField()
    dob = models.DateField(blank=True)
    is_Moderator = models.BooleanField(default=False)
    #is_active = BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    #is_superuser = BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    has_subscribed = models.BooleanField(default=False)
    #bookmarksList = ListField(ObjectIdField(), default = list)
    #USERNAME_FIELD = 'username'
    #REQUIRED_FIELDS = []

    objects = UserCustomManager()

    def __str__(self):
        return self.username
    class Meta:
       # db_table = 'auth_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'    
