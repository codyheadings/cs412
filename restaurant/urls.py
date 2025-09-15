# file: restaurant/urls.py
# author: Cody Headings, codyh@bu.edu, 9/15/2025
# desc: url navigation patterns for routes in restaurant app

from django.urls import path
from django.conf import settings
from . import views

# URL patterns specific to the restaurant app
urlpatterns = [
    path(r'', views.main, name="main"),
    path(r'main', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),
]