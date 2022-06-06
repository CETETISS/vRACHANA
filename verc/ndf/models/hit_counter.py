from django.db import models

class hit_counter(models.Model):
    #id =  models.IntegerField(primary_key=True)
    visitednode_name = models.CharField(max_length=30)
    visitednode_id = models.CharField(max_length=30)
    created_date = models.DateField()
    preview_count = models.IntegerField()
    visit_count = models.IntegerField()
    download_count = models.IntegerField()
    session_id = models.CharField(max_length=30)
    last_updated = models.DateField()
    class Meta:
        db_table = 'hit_counters'

