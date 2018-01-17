from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class history(models.Model) :
    search_id = models.AutoField(primary_key=True)
    search_keyword = models.CharField(max_length=255)
    search_user = models.CharField(max_length=255, default='Anonymous')
    search_time = models.DateTimeField(auto_now_add=True)
    search_imagelist = models.CharField(max_length=255, default='Error')
    search_namelist = models.CharField(max_length=255, default='Error')
    search_pricelist = models.CharField(max_length=255, default='Error')
    search_shoplist = models.CharField(max_length=255, default='Error')
    search_linklist = models.CharField(max_length=255, default='Error')

class userhint(models.Model) :
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    user_hint = models.CharField(max_length=100)