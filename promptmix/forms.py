# file: promptmix/forms.py
# author: Cody Headings, codyh@bu.edu, 11/30/2025
# desc: definitions for forms to be used in views

from django import forms
from .models import *

class CreatePromptForm(forms.ModelForm):
    """A form to add a new Prompt to the database."""

    class Meta:
        """Associate this form with a model from the database"""
        model=Prompt
        fields = ["subject", "text"]

class CreateRemixForm(forms.ModelForm):
    """A form to add a new Remix to the database."""

    class Meta:
        model = Remix
        fields = ["text"]

class UpdateProfileForm(forms.ModelForm):
    """A form to update a profile in the database."""

    class Meta:
        """Associate this form with a model from the database"""
        model=Profile
        fields = ["display_name", "profile_image_url"]

class UpdatePromptForm(forms.ModelForm):
    """A form to update a post in the database."""

    class Meta:
        """Associate this form with a model from the database"""
        model=Prompt
        fields = ["subject", "text"]

# class CreateProfileForm(forms.ModelForm):
#     """A form to create a new profile in the database."""

#     class Meta:
#         """Associate this form with a model from the database"""
#         model=Profile
#         fields = ["username", "display_name", "bio_text", "profile_image_url"]