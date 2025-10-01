# file: mini_insta/urls.py
# author: Cody Headings, codyh@bu.edu, 9/25/2025
# desc: url pattern routes for app navigation

from django.urls import path
from .views import *

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name='create_post'),
]