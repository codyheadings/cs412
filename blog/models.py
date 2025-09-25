# blog/models.py
# Define the data objects for our application
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.title} by {self.author}'