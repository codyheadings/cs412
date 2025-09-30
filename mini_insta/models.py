# file: mini_insta/models.py
# author: Cody Headings, codyh@bu.edu, 9/25/2025
# desc: definitions for data models

from django.db import models
from django.urls import reverse

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
    
    def get_absolute_url(self):
        """Return a URL to display one instance of this model."""
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def has_posts(self):
        """Return true if user has posts, false otherwise"""
        posts = Post.objects.filter(profile=self)
        return len(posts)>0
    
    def get_all_posts(self):
        """Return a QuerySet of Posts from this user."""
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts
    
class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'Post by {self.profile} at {self.timestamp}'
    
    def has_photos(self):
        """Return true if post has photos, false otherwise"""
        photos = Photo.objects.filter(post=self)
        return len(photos)>0
    
    def get_all_photos(self):
        """Return a QuerySet of Photos attached to this Post."""
        photos = Photo.objects.filter(post=self)
        return photos
    
class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'Photo from {self.post}'