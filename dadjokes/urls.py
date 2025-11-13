# file: dadjokes/urls.py
# author: Cody Headings, codyh@bu.edu, 11/11/2025
# desc: url pattern routes for app navigation

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', ProfileListView.as_view(), name='show_all_profiles'),
]