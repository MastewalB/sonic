from django.db import models

class Search(models.Model):
    search_query = models.CharField(max_length=100)
    search_type = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
