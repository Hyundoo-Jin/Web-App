from django.conf.urls import url
from django.contrib import admin
from search import views as sc_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', sc_views.index, name='index'),
    url(r'^history$', sc_views.take_history, name='history'),
    url(r'^search_process$', sc_views.search_process, name='search_process'),
    url(r'^result/(?P<keyword>.+)$', sc_views.search_result, name='search_result'),
    url(r'^check_login', sc_views.check_login, name='check_login'),
    url(r'^registration$', sc_views.registration, name='registration'),
    url(r'^registration_process$', sc_views.registration_process, name='registration_process'),
    url(r'^account_info$', sc_views.account_info, name='account_info'),
    url(r'^logout$', sc_views.logout, name='logout'),
]
