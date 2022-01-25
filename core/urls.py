# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include, re_path  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls")),
    re_path(r'^celery-progress/', include('celery_progress.urls')),             # UI Kits Html files
]
