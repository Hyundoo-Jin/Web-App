from django.contrib import admin

# Register your models here.

from .models import history
from search.models import shops

class historyadmin(admin.ModelAdmin) :
    list_display = ['search_user', 'search_keyword', 'first', 'second', 'third', 'fourth', 'fifth', 'search_time']
    list_display_links = ['search_user', 'search_keyword', 'search_time']
    list_filter = ['search_user', 'search_time']
    list_per_page = 10

    def first(self, history):
        try :
            return history.search_namelist.split(',')[0]
        except :
            return '결과없음'
    def second(self, history):
        try :
            return history.search_namelist.split(',')[1]
        except :
            return '결과없음'
    def third(self, history):
        try :
            return history.search_namelist.split(',')[2]
        except :
            return '결과없음'
    def fourth(self, history):
        try :
            return history.search_namelist.split(',')[3]
        except :
            return '결과없음'
    def fifth(self, history):
        try :
            return history.search_namelist.split(',')[4]
        except :
            return '결과없음'

admin.site.register(history, historyadmin)

class shophistory(admin.ModelAdmin) :
    list_display = ['date', 'first_shop']
    list_filter = ['date', 'first_shop']
    list_per_page = 10

admin.site.register(shops, shophistory)