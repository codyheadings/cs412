# file: mini_insta/views.py
# author: Cody Headings, codyh@bu.edu, 9/25/2025
# desc: view functions to return html renders

from django.shortcuts import render
from mini_insta.forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.
class ProfileListView(ListView):
    """Create a subclass of ListView to display all profile pages."""
    
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

    def get_object(self):
        """Override default method to get object from current user."""
        # find the logged in user
        user = self.request.user

        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
        else:
            profile = None
        return profile

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data()
 
        # find/add the profile to the context data
        profile = self.get_object()
        if profile != None:
            # add this profile into the context dictionary:
            context['profile'] = profile
        return context

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

class CreatePostView(LoginRequiredMixin, CreateView):
    '''A view to create a new post and save it to the database.'''
 
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_object(self):
        """Override default method to get object from current user."""

        # find the logged in user
        user = self.request.user

        profile = Profile.objects.get(user=user)

        return profile

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data()
 
        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        # pk = self.kwargs['pk']
        profile = self.get_object()
 
        # add this profile into the context dictionary:
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

        # image_url = self.request.POST.get("image_url")  # grab URL from form
        # if image_url:
        #     Photo.objects.create(post=form.instance, image_url=image_url)

        self.object = form.save()
        files = self.request.FILES.getlist('image_file')
        for f in files:
            Photo.objects.create(post=form.instance, image_file=f)
 
        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirects to new post page after successful creation."""
        return reverse('show_post', kwargs={'pk':self.object.pk})
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """View class to handle update of a profile based on its pk."""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self):
        """Override default method to get object from current user."""

        # find the logged in user
        user = self.request.user

        profile = Profile.objects.get(user=user)

        return profile

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

class UpdatePostView(LoginRequiredMixin, UpdateView):
    """View class to handle update of a post based on its pk."""

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

class DeletePostView(LoginRequiredMixin, DeleteView):
    '''A view to delete a Post and remove it from the database.'''
 
    template_name = "mini_insta/delete_post_form.html"
    model = Post
    context_object_name = 'post'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_context_data(self, **kwargs):
        """Provides context data to the delet post form."""

        # calling the superclass method
        context = super().get_context_data(**kwargs)
        # get current post object
        post = self.object
        profile = post.profile
 
        # add this profile into the context dictionary:
        context['profile'] = profile
        context['post'] = post
        return context

    def get_success_url(self):
        """Return url to redirect to after delete."""

        # get the pk for this post
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        
        # find the profile to which this Post is related by FK
        profile = post.profile
        
        # reverse to show the profile page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
class ShowFollowersDetailView(DetailView):
    """Subclass of DetailView to display a profile's followers."""
    
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    """Subclass of DetailView to display who a Profile is following."""
    
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class PostFeedListView(LoginRequiredMixin, ListView):
    """Create a subclass of ListView to display post feed for a profile."""
    
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_object(self):
        """Override default method to get object from current user."""

        # find the logged in user
        user = self.request.user

        profile = Profile.objects.get(user=user)

        return profile

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_queryset(self):
        """Return the feed posts from followed profiles."""
        profile = Profile.objects.get(user=self.request.user)
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """Add the profile object to the context data."""
        context = super().get_context_data(**kwargs)

        profile = self.get_object()

        context['profile'] = profile
        return context
    
class SearchView(LoginRequiredMixin, ListView):
    """Subclass of ListView to display Post and Profile search results."""
    
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def get_object(self):
        """Override default method to get object from current user."""

        # find the logged in user
        user = self.request.user

        profile = Profile.objects.get(user=user)

        return profile

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Method called to handle any request."""
        # get search query and profile and store in object
        self.query = self.query = self.request.GET.get('query')
        self.profile = self.get_object()

        if(not self.query):
            return render(request, 'mini_insta/search.html', {'profile': self.profile})
        else:
            return super().dispatch(request, *args, **kwargs)
        
    def get_queryset(self):
        if not self.query:
            return Post.objects.none()
        return Post.objects.filter(caption__icontains=self.query).order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        """Add profile, query, and search results to context data."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        context['query'] = self.query

        # If there is a search query, use OR logic to filter results
        if self.query:
            matches = Profile.objects.filter(
                Q(username__icontains=self.query) 
                | Q(display_name__icontains=self.query) 
                | Q(bio_text__icontains=self.query)
            )
        else:
            matches = Profile.objects.none()

        context['matches'] = matches
        return context
    
class LoginRequiredSubclass(LoginRequiredMixin):
    """Subclass of LoginRequiredMixin with specific mini_insta functions."""

    def get_logged_in_profile(self):
        """Returns the profile object for the logged in user."""

        # find the logged in user
        user = self.request.user

        profile = Profile.objects.get(user=user)

        return profile
    
    def get_login_url(self):
        return
    
class CreateProfileView(CreateView):
    """A view to create a new profile and save it to the database."""

    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
 
        # add UserCreationForm into the context dictionary:
        context['user_form'] = UserCreationForm
        return context
    
    def form_valid(self, form):
        '''Handles the form submission and saves the 
        new object to the Django database.
        '''

        print(f"CreateProfileView.form_valid: cleaned_data={form.cleaned_data}")
        
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
 
        form.instance.user = user

        # delegate to the superclass method form_valid:
        return super().form_valid(form)