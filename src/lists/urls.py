from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^the-only-list-in-the-world/$', views.view_list, name='view_list'),
    url(r'^new$', views.new_list, name='new_list'),
]
