from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class history(models.Model) :
    search_id = models.AutoField(primary_key=True)
    search_keyword = models.CharField(max_length=255)
    search_user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_time = models.DateTimeField(auto_now_add=True)
    search_first = models.CharField(max_length=50)
    search_second = models.CharField(max_length=50, default=None)
    search_third = models.CharField(max_length=50, default=None)
    search_fourth = models.CharField(max_length=50, default=None)
    search_fifth = models.CharField(max_length=50, default=None)

class userhint(models.Model) :
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    user_hint = models.CharField(max_length=100)