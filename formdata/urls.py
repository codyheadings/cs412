# file: quotes/urls.py
# author: Cody Headings, codyh@bu.edu, 9/15/2025
# desc: url navigation patterns for routes in form app

from django.urls import path
from django.conf import settings
from . import views

# URL patterns specific to the formdata app
urlpatterns = [
    path(r'', views.show_form, name="show_form"),
    path(r'submit', views.submit, name="submit"),
]