# blog/models.py
# Define the data objects for our application
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    # image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        """Return a URl to display one instance of this model."""
        return reverse('article', kwargs={'pk': self.pk})
    
    def get_all_comments(self):
        """Return a QuerySet of comments abour this article."""
        comments = Comment.objects.filter(article=self)
        return comments
    
class Comment(models.Model):
    """Encapsulate the idea of a comment on an article."""

    # data attributs for the Comment:
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Comment."""
        return f'{self.text}'