# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from .views import google_trends
from django.conf.urls import url


urlpatterns = [

    # The home page
    path('', google_trends, name='trends'),
    url(r'^(?P<task_id>[\w-]+)/$', google_trends, name='task_status'),
    #path('', views.index, name='home'),
    

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
