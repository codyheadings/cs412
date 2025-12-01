# file: promptmix/urls.py
# author: Cody Headings, codyh@bu.edu, 11/27/2025
# desc: url pattern routes for app navigation

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
    path('prompt/<int:pk>', PromptDetailView.as_view(), name='show_prompt'),
    path('profile/<int:pk>/create_prompt', CreatePromptView.as_view(), name='create_prompt'),
    path("prompt/<int:prompt_id>/remix", CreateRemixView.as_view(), name="create_prompt_remix"),
    path("remix/<int:remix_id>/remix", CreateRemixView.as_view(), name="create_remix_remix"),
    path('feed', PromptFeedListView.as_view(), name='show_feed'),
]