# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views as accoutns_views


urlpatterns = [
    url(r'^login$', accoutns_views.persona_login, name="persona_login"),
]
