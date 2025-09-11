# file: quotes/urls.py
# author: Cody Headings, codyh@bu.edu, 9/9/2025
# desc: url navigation patterns for routes in quotes app

from django.urls import path
from django.conf import settings
from . import views

# URL patterns specific to the quotes app
urlpatterns = [
    path(r'', views.quote, name="quote"),
    path(r'quote', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"),
    path(r'about', views.about, name="about"),
]