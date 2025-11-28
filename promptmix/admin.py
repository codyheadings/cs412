# file: promptmix/admin.py
# author: Cody Headings, codyh@bu.edu, 11/25/2025
# desc: register models to admin route

from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Profile)
admin.site.register(Prompt)
admin.site.register(Remix)
admin.site.register(Follow)
admin.site.register(Boost)