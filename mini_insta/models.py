# file: mini_insta/models.py
# author: Cody Headings, codyh@bu.edu, 9/25/2025
# desc: definitions for data models

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    """Model to store attributes of a user profile."""
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now_add=True)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'@{self.username}'
    
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
    
    def get_post_count(self):
        """Return number of Posts from this user."""
        numposts = len(Post.objects.filter(profile=self))
        return numposts
    
    def get_followers(self):
        """Return a list of Profiles that Follow this Profile."""
        followers = Follow.objects.filter(profile=self).values("follower_profile")
        return list(Profile.objects.filter(id__in=followers))
    
    def get_num_followers(self):
        """Return number of followers following this profile."""
        numfollowers = len(Follow.objects.filter(profile=self))
        return numfollowers
    
    def get_following(self):
        """Return a list of Profiles that are Followed by this Profile."""
        following = Follow.objects.filter(follower_profile=self).values("profile")
        return list(Profile.objects.filter(id__in=following))
    
    def get_num_following(self):
        """Return number of profiles followed by this profile."""
        numfollowing = len(Follow.objects.filter(follower_profile=self))
        return numfollowing
    
class Post(models.Model):
    """Model that represents a single post for a user."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'Post by {self.profile} at {self.timestamp}'
    
    def get_absolute_url(self):
        """Return a URL to display one instance of this model."""
        return reverse('show_post', kwargs={'pk': self.pk})
    
    def has_photos(self):
        """Return true if post has photos, false otherwise"""
        photos = Photo.objects.filter(post=self)
        return len(photos)>0
    
    def get_all_photos(self):
        """Return a QuerySet of Photos attached to this Post."""
        photos = Photo.objects.filter(post=self)
        return photos
    
    def get_all_comments(self):
        """Return a QuerySet of Comments attached to this Post."""
        comments = Comment.objects.filter(post=self)
        return comments
    
    def get_all_likes(self):
        """Return a QuerySet of Likes on this Post."""
        likes = Like.objects.filter(post=self).order_by('-timestamp')
        return likes
    
    def display_likes(self):
        """Displays the Post's Likes in a friendly way."""
        likes = self.get_all_likes()
        total_likes = len(likes)

        if total_likes == 0:
            return "Be the first to like this post!"
        elif total_likes == 1:
            return f"Liked by {likes.first().profile}"
        elif total_likes == 2:
            first = likes[0]
            second = likes[1]
            return f"Liked by {first.profile} and {second.profile}"
        else:
            first_like = likes.first()
            others = total_likes - 1
            return f"Liked by {first_like.profile} and {others} others"

class Photo(models.Model):
    """Model that represents an image attached to a user's post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        if self.image_url != "":
            ptype = "URL"
        else:
            ptype = "file"
        
        val = "Photo " + ptype + f" from {self.post}"

        return val
    
    def get_image_url(self):
        """Returns the url to the image object."""
        if self.image_url != "":
            return self.image_url
        else:
            return self.image_file.url
            
class Follow(models.Model):
    """Model that represents a connection between two profiles."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of this Follow connection"""
        return f"{self.follower_profile} follows {self.profile}"
    
class Comment(models.Model):
    """Model that represents a comment on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    def __str__(self):
        """Return string representation of this comment."""
        return f"{self.profile} commented \"{self.text}\" on {self.post}"
    
class Like(models.Model):
    """Model that represents a person showing approval of a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of this comment."""
        return f"{self.profile} liked {self.post}"