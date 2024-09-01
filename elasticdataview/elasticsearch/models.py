from django.db import models


class Elasticsearch(models.Model):
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    scheme = models.CharField(choices=[('http', 'http'), ('https', 'https')], max_length=255)


    class Meta:
        db_table = 'Elasticsearch'
