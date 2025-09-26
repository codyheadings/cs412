# file: mini_insta/views.py
# author: Cody Headings, codyh@bu.edu, 9/25/2025
# desc: view functions to return html renders

from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView
import random

# Create your views here.
class ProfileListView(ListView):
    """Create a subclass of ListView to display all profile pages."""
    
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    """Subclass of DetailView to display a single profile page."""
    
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'