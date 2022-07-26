# imports from python libraries
import os
import hashlib
import datetime
import json
import magic
import mimetypes
import io

from itertools import chain     # Using from_iterable()
from hashfs import HashFS       # content-addressable file management system
#from StringIO import StringIO
from PIL import Image
from django.utils import timezone

# imports from installed packages
#from django.contrib.auth import get_user_model
#User = get_user_model()
#from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.sessions.models import Session
from django.db import models
from django.http import HttpRequest
#from celery import task
from django.template.defaultfilters import slugify
from django.core.cache import cache

#from django_mongokit import connection
#from django_mongokit import get_database
#from django_mongokit.document import DjangoDocument
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError

#from mongoengine import connection
#from mongoengine import document
#from mongoengine import get_db
from mongoengine import *

import pymongo

#MONGODB_HOST = 'mongodb://127.0.0.1:27017'
#con = connect(db='verc_db', host=MONGODB_HOST)

#from mongokit import IS, OR
#from mongokit import INDEX_ASCENDING, INDEX_DESCENDING

try:
    from bson import ObjectId
except ImportError:  # old pymongo
    from pymongo.objectid import ObjectId

from ndf.views.utils import add_to_list, cast_to_data_type

#from registration.signals import user_registered

# imports from application folders/files
from verc.settings import MEDIA_ROOT
#from verc.settings import RCS_REPO_DIR,RCS_REPO_DIR_HASH_LEVEL
from verc.settings import MARKUP_LANGUAGE
from verc.settings import MARKDOWN_EXTENSIONS
from verc.settings import GSTUDIO_GROUP_AGENCY_TYPES, GSTUDIO_GROUP_AGENCY_TYPES_DEFAULT, GSTUDIO_AUTHOR_AGENCY_TYPES
from verc.settings import GSTUDIO_DEFAULT_COPYRIGHT, GSTUDIO_DEFAULT_LICENSE
from verc.settings import META_TYPE
#from verc.settings import GSTUDIO_BUDDY_LOGIN
#from verc.ndf.rcslib import RCS
#from gnowsys_ndf.ndf.views.utils import add_to_list, cast_to_data_type
# from gnowsys_ndf.ndf.views.es_queries import *


NODE_TYPE_CHOICES = (
    ('Nodes'),
    ('Attribute Types'),
    ('Attributes'),
    ('Relation Types'),
    ('Relations'),
    ('GSystem Types'),
    ('GSystems'),
    ('Attribute Specification'),
    ('Relation Specification'),
)

NODE_ACCESS_POLICY = (
    ('PUBLIC'),
    ('PRIVATE')
)

TYPES_OF_GROUP = (
    ('PUBLIC'),
    ('PRIVATE'),
    ('ANONYMOUS')
)
TYPES_OF_GROUP_DEFAULT = 'PUBLIC'

EDIT_POLICY = (
    ('EDITABLE_NON_MODERATED'),
    ('EDITABLE_MODERATED'),
    ('NON_EDITABLE')
)
EDIT_POLICY_DEFAULT = 'EDITABLE_NON_MODERATED'
'''
SUBSCRIPTION_POLICY = (
    ('OPEN'),
    ('BY_REQUEST'),
    ('BY_INVITATION'),
)
SUBSCRIPTION_POLICY_DEFAULT = 'OPEN'
'''
EXISTANCE_POLICY = (
    ('ANNOUNCED'),
    ('NOT_ANNOUNCED')
)
EXISTANCE_POLICY_DEFAULT = 'ANNOUNCED'
'''
LIST_MEMBER_POLICY = (
    ('DISCLOSED_TO_MEM'),
    ('NOT_DISCLOSED_TO_MEM')
)
LIST_MEMBER_POLICY_DEFAULT = 'DISCLOSED_TO_MEM'

ENCRYPTION_POLICY = (
    ('NOT_ENCRYPTED'),
    ('ENCRYPTED')
)
ENCRYPTION_POLICY_DEFAULT = 'NOT_ENCRYPTED'
'''

DATA_TYPE_CHOICES = (
    "None",
    "bool",
    "basestring",
    "unicode",
    "int",
    "float",
    "long",
    "datetime.datetime",
    "list",
    "dict",
    "ObjectId",
    "IS()"
)

TYPES_LIST = ['GSystemType', 'RelationType', 'AttributeType', 'MetaType', 'ProcessType']

my_doc_requirement = u'storing_orignal_doc'
reduced_doc_requirement = u'storing_reduced_doc'
to_reduce_doc_requirement = u'storing_to_be_reduced_doc'
indexed_word_list_requirement = u'storing_indexed_words'

# CUSTOM DATA-TYPE DEFINITIONS
#STATUS_CHOICES_TU = IS(u'DRAFT', u'HIDDEN', u'PUBLISHED', u'DELETED', u'MODERATION')
#STATUS_CHOICES = tuple(str(qtc) for qtc in STATUS_CHOICES_TU)

#QUIZ_TYPE_CHOICES_TU = IS(u'Short-Response', u'Single-Choice', u'Multiple-Choice')
#QUIZ_TYPE_CHOICES = tuple(str(qtc) for qtc in QUIZ_TYPE_CHOICES_TU)

# Designate a root folder for HashFS. If the folder does not exists already, it will be created.
# Set the `depth` to the number of subfolders the file's hash should be split when saving.
# Set the `width` to the desired width of each subfolder.
gfs = HashFS(MEDIA_ROOT, depth=3, width=1, algorithm='sha256')
# gfs: gstudio file system

# DATABASE Variables
db = get_db()
