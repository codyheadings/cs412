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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='promptmix_profile')

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.display_name}'
    
    def get_absolute_url(self):
        """Return a URL to display one instance of this model."""
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def has_prompts(self):
        """Return true if user has prompts, false otherwise"""
        prompts = Prompt.objects.filter(profile=self)
        return len(prompts)>0
    
    def get_all_prompts(self):
        """Return a QuerySet of Prompts from this user."""
        prompts = Prompt.objects.filter(profile=self)
        return prompts
    
    def get_prompt_count(self):
        """Return number of Prompts from this user."""
        numprompts = len(Prompt.objects.filter(profile=self))
        return numprompts
    
    def get_remix_count(self):
        """Return number of Remixes from this user."""
        numremixes = len(Remix.objects.filter(profile=self))
        return numremixes
    
    def get_total_words(self):
        """Return total number of words in all remixes."""
        remixes = Remix.objects.filter(profile=self)
        total = 0
        for remix in remixes:
            total += remix.word_count()
        return total
    
    def get_avg_words(self):
        """Return avg number of words per remix."""
        total=self.get_total_words()
        numremixes = self.get_remix_count()
        if numremixes>0:
            return total/numremixes
        else:
            return 0.0
    
class Prompt(models.Model):
    """Model that represents a single posted prompt for a Profile."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) 
    # TODO: Change delete behavior, cascade isn't desired in this situation
    # We want to check if there are any remixes of this prompt, if not delete it
    # But if so, we want to archive it and lock the thread to new replies
    timestamp = models.DateTimeField(auto_now_add=True)
    subject = models.TextField(blank=False)
    text = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.subject} by {self.profile}'
    
    def get_absolute_url(self):
        """Return a URL to display one instance of this model."""
        return reverse('show_prompt', kwargs={'pk': self.pk})
    
    def get_all_remixes(self):
        """Return a QuerySet of all Remixes directly attached to this Prompt."""
        remixes = Remix.objects.filter(prompt=self, remix__isnull=True)
        return remixes
    
    def get_pk(self):
        return self.pk
    
    def get_all_boosts(self):
        """Return a QuerySet of Boosts on this Prompt."""
        boosts = Boost.objects.filter(prompt=self)
        return boosts
            
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

    def get_absolute_url(self):
        """Return a URL to redirect user to prompt page where the remix is."""
        return reverse('show_prompt', kwargs={'pk': self.prompt.pk})

    def __str__(self):
        """Return string representation of this comment."""
        if self.remix:
            post = self.remix
        else:
            post = self.prompt
        return f"Re: {post}"
    
    def get_all_boosts(self):
        """Return a QuerySet of Boosts on this Prompt."""
        boosts = Boost.objects.filter(remix=self)
        return boosts
    
    def word_count(self):
        words = self.text.split()
        return len(words)
    
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