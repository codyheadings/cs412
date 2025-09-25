# file: mini_insta/urls.py
# author: Cody Headings, codyh@bu.edu, 9/25/2025
# desc: url pattern routes for app navigation

from django.urls import path
from .views import ProfileListView

urlpatterns = [
    # path('', RandomArticleView.as_view(), name='random'),
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    # path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
]