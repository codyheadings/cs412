# file: mini_insta/views.py
# author: Cody Headings, codyh@bu.edu, 9/25/2025
# desc: view functions to return html renders

from django.shortcuts import render
from mini_insta.forms import CreatePostForm
from .models import *
from django.views.generic import ListView, DetailView, CreateView
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

class PostDetailView(DetailView):
    """Subclass of DetailView to display a single post page."""
    
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    '''A view to create a new post and save it to the database.'''
 
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data()
 
        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
 
 
        # add this article into the context dictionary:
        context['profile'] = profile
        return context
 
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        Adds the foreign key (of the Profile) to the Post
        object before saving it to the database.
        '''
 
		# instrument our code to display form fields: 
        print(f"CreatePostView.form_valid: cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this profile to the post
        form.instance.profile = profile # set the FK

        image_url = self.request.POST.get("image_url")  # grab URL from form
        if image_url:
            Photo.objects.create(post=form.instance, image_url=image_url)
 
        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)