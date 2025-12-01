# file: promptmix/models.py
# author: Cody Headings, codyh@bu.edu, 11/25/2025
# desc: definitions for data models

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    """Model to store attributes of a user profile."""
    display_name = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now_add=True)
    profile_image_url = models.URLField(blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='promptmix_profile')

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.display_name}'
    
    # May be useful later
    # def get_absolute_url(self):
    #     """Return a URL to display one instance of this model."""
    #     return reverse('show_profile', kwargs={'pk': self.pk})
    
    # def has_posts(self):
    #     """Return true if user has posts, false otherwise"""
    #     posts = Post.objects.filter(profile=self)
    #     return len(posts)>0
    
    # def get_all_posts(self):
    #     """Return a QuerySet of Posts from this user."""
    #     posts = Post.objects.filter(profile=self).order_by('-timestamp')
    #     return posts
    
    # def get_post_count(self):
    #     """Return number of Posts from this user."""
    #     numposts = len(Post.objects.filter(profile=self))
    #     return numposts
    
    # def get_post_feed(self):
    #     """Returns a list of posts personalized for the profile."""
    #     posts = []
    #     followed_profiles = self.get_following()
    #     for profile in followed_profiles:
    #         posts += profile.get_all_posts()

    #     posts.sort(key=lambda post: post.timestamp, reverse=True)
    #     return posts
    
class Prompt(models.Model):
    """Model that represents a single posted prompt for a Profile."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) 
    # TODO: Change delete behavior, cascade isn't desired in this situation
    # We want to check if there are any remixes of this prompt, if not delete it
    # But if so, we want to keep it up but lock the thread to new replies
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.TextField(blank=False)
    text = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.subject} by {self.profile}'
    
    # def get_absolute_url(self):
    #     """Return a URL to display one instance of this model."""
    #     return reverse('show_post', kwargs={'pk': self.pk})
    
    def get_all_remixes(self):
        """Return a QuerySet of all Remixes directly attached to this Prompt."""
        remixes = Remix.objects.filter(prompt=self, remix__isnull=True)
        return remixes
    
    # def get_all_likes(self):
    #     """Return a QuerySet of Likes on this Post."""
    #     likes = Like.objects.filter(post=self).order_by('-timestamp')
    #     return likes
            
class Follow(models.Model):
    """
    Model that represents a user wishing to save another 
    user's Prompt for later or stay updated on its content.
    """
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of this Follow connection"""
        return f"{self.follower_profile} follows {self.prompt}"
    
class Remix(models.Model):
    """Model that represents a reply to a Prompt or other Remix."""
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, blank=True, null=True, related_name='remixed_prompt')
    remix = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    # TODO: Change delete behavior, cascade isn't desired in this situation
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    def __str__(self):
        """Return string representation of this comment."""
        if self.remix:
            post = self.remix
        else:
            post = self.prompt
        return f"Re: {post}"
    
class Boost(models.Model):
    """Model that represents a user showing approval of a Prompt or Remix."""
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, blank=True, null=True, related_name='boosted_prompt')
    remix = models.ForeignKey(Remix, on_delete=models.CASCADE, blank=True, null=True, related_name='boosted_remix')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of this comment."""
        if self.prompt:
            post = self.prompt
        else:
            post = self.remix
        return f"{self.profile} boosted {post}"
    
#class Pin(models.Model):