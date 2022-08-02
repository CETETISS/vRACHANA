from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from .managers import UserCustomManager


class User(AbstractUser):
    fullname = models.CharField(max_length=100)
    dob = models.DateField(blank=True)
    is_Moderator = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    has_subscribed = models.BooleanField(default=False)
    role = models.CharField(max_length=100,blank=True)
    def __str__(self):
        return self.username
    