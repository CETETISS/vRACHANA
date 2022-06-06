from base_imports import *
class Benchmark(Document):

  #objects = models.Manager()

  collection_name = 'Benchmarks'
  _type = StringField()
  name = StringField(Required = True)
  time_taken = StringField()
  parameters = StringField()
  size_of_parameters = StringField()
  function_output_length = StringField()
  calling_url = StringField()
  last_update = DateTimeField()
  action = StringField()
  user = StringField()
  session_key = StringField()
  group = StringField()
  has_data = DictField()
  locale = StringField()
  
  def __unicode__(self):
    return self._id

  def identity(self):
    return self.__unicode__()


benchmark_collection= db["Benchmarks"]
