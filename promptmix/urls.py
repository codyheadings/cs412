# file: promptmix/urls.py
# author: Cody Headings, codyh@bu.edu, 11/27/2025
# desc: url pattern routes for app navigation

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
    path('prompt/<int:pk>', PromptDetailView.as_view(), name='show_prompt'),
    path('prompt/<int:pk>/update', UpdatePromptView.as_view(), name='update_prompt'),
    path('prompt/<int:pk>/boost', BoostPromptView.as_view(), name='create_prompt_boost'),
    path('prompt/<int:pk>/follow', CreateFollowView.as_view(), name='create_follow'),
    path('prompt/<int:pk>/delete_boost', DeletePromptBoostView.as_view(), name='delete_prompt_boost'),
    path('prompt/<int:pk>/delete_follow', DeleteFollowView.as_view(), name='delete_follow'),
    path('remix/<int:pk>/update', UpdateRemixView.as_view(), name='update_remix'),
    path('remix/<int:pk>/boost', BoostRemixView.as_view(), name='create_remix_boost'),
    path('remix/<int:pk>/delete_boost', DeleteRemixBoostView.as_view(), name='delete_remix_boost'),
    path('profile/create_prompt', CreatePromptView.as_view(), name='create_prompt'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/followed', FollowedPromptsListView.as_view(), name='show_followed'),
    path("prompt/<int:prompt_id>/remix", CreateRemixView.as_view(), name="create_prompt_remix"),
    path("remix/<int:remix_id>/remix", CreateRemixView.as_view(), name="create_remix_remix"),
    path('', PromptFeedListView.as_view(), name='show_feed'),
    path('feed', PromptFeedListView.as_view(), name='show_feed'),
    path('login/', auth_views.LoginView.as_view(template_name='promptmix/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_feed'), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
]