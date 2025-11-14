# file: dadjokes/urls.py
# author: Cody Headings, codyh@bu.edu, 11/11/2025
# desc: url pattern routes for app navigation

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', RandomView.as_view(), name='random'),
    path('random', RandomView.as_view(), name='random'),
    path('jokes', JokeListView.as_view(), name='show_all_jokes'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='show_joke'),
    path('pictures', PictureListView.as_view(), name='show_all_pictures'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='show_picture'),
    path(r'api/', RandomJokeAPIView.as_view(), name="random_joke_api"),
    path(r'api/random/', RandomJokeAPIView.as_view(), name="random_joke_api"),
    path(r'api/random_picture/', RandomPictureAPIView.as_view(), name="random_picture_api"),
    path(r'api/jokes/', JokeListAPIView.as_view(), name="joke_list_api"),
    # path(r'api/joke/<int:pk>', JokeDetailAPIView.as_view(), name="joke_detail_api"),
    path(r'api/pictures/', PictureListAPIView.as_view(), name="picture_list_api"),
    # path(r'api/pictures/<int:pk>', PictureDetailAPIView.as_view(), name="picture_detail_api"),
]