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

    def __str__(self):
        return str(self.search_user) + '-' + str(self.search_keyword)

class userhint(models.Model) :
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    user_hint = models.CharField(max_length=100)

class shops(models.Model) :
    date = models.DateField(auto_now_add=True)
    first_shop = models.TextField(max_length=255, default='없음')
    count = models.IntegerField(max_length=255, default=1)