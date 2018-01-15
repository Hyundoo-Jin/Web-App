from django.conf.urls import url
from django.contrib import admin
from search import views as sc_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', sc_views.index, name='index'),
    url(r'^history$', sc_views.take_history, name='history'),
    url(r'^search/$', sc_views.search, name='search'),
]
