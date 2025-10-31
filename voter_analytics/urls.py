# file: voter_analytics/urls.py
# author: Cody Headings, codyh@bu.edu, 10/30/2025
# desc: url pattern routes for app navigation

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
]