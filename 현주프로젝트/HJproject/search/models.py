from django.db import models

# Create your models here.
class history(models.Model) :
    search_id = models.AutoField(primary_key=True)
    search_keyword = models.CharField(max_length=255)
    search_user = models.CharField(max_length=100, default='Unknown')
    search_time = models.DateTimeField()
    search_first = models.CharField(max_length=50)
    search_second = models.CharField(max_length=50, default=None)
    search_third = models.CharField(max_length=50, default=None)
    search_fourth = models.CharField(max_length=50, default=None)
    search_fifth = models.CharField(max_length=50, default=None)