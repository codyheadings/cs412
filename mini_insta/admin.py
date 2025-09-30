# file: mini_insta/admin.py
# author: Cody Headings, codyh@bu.edu, 9/25/2025
# desc: register models to admin route

from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)