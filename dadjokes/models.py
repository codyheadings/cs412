# file: dadjokes/models.py
# author: Cody Headings, codyh@bu.edu, 11/11/2025
# desc: definitions for data models
from django.db import models

# Create your models here.
class Joke(models.Model):
    """Model that represents a dad joke in the database."""
    text = models.TextField(blank=False)
    name = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class Picture(models.Model):
    """Model that represents a silly picture in the database."""
    image_url = models.URLField(blank=False)
    name = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)