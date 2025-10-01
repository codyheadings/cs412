# file: mini_insta/forms.py
# author: Cody Headings, codyh@bu.edu, 9/30/2025
# desc: definitions for data models

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """A form to add a new Post to the database."""

    class Meta:
        """Associaate this form with a model from the database"""
        model=Post
        fields = ["caption"]