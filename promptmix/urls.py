# file: promptmix/urls.py
# author: Cody Headings, codyh@bu.edu, 11/27/2025
# desc: url pattern routes for app navigation

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
    path('prompt/<int:pk>', PromptDetailView.as_view(), name='show_prompt'),
]