from .base_imports import *

#@connection.register
class Analytics(Document):

  objects = models.Manager()

  collection_name = 'analytics_collection'

  timestamp=DateTimeField(Required = True)
  action=DictField() 
  user=DictField()
  obj=DictField()
  group_id=StringField()
  session_key=StringField()

  
  def __unicode__(self):
    return self._id

  def identity(self):
    return self.__unicode__()
