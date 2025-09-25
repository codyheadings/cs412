# file: mini_insta/models.py
# author: Cody Headings, codyh@bu.edu, 9/25/2025
# desc: definitions for data models

from django.db import models

# Create your models here.
class Profile(models.Model):
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'user @{self.username}'