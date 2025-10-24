# file: mini_insta/views.py
# author: Cody Headings, codyh@bu.edu, 9/25/2025
# desc: view functions to return html renders

from django.shortcuts import render
from mini_insta.forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
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

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data()
 
        # check if user is following this profile
        user = self.request.user

        if user.is_authenticated:
            user_profile = Profile.objects.get(user=user)
            page_profile = Profile.objects.get(pk=self.kwargs["pk"])

            is_following = Follow.objects.filter(profile=page_profile, follower_profile=user_profile)
            
            if is_following.exists():
                context['is_following'] = "true"

        return context

class PostDetailView(DetailView):
    """Subclass of DetailView to display a single post page."""
    
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data()
 
        # check if user has liked this post
        user = self.request.user

        if user.is_authenticated:
            user_profile = Profile.objects.get(user=user)
            post = Post.objects.get(pk=self.kwargs["pk"])

            is_liked = Like.objects.filter(profile=user_profile, post=post)
            
            if is_liked.exists():
                context['is_liked'] = "true"

        return context

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
    
class FollowProfileView(LoginRequiredMixin, TemplateView):
    """A view to have the logged in user follow another user's profile."""

    template_name="mini_insta/follow.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Accepts HTTP request and handles response logic."""

        user = self.request.user
        if user.is_authenticated:
            follower_profile = Profile.objects.get(user=user)

            followed_profile = Profile.objects.get(pk=self.kwargs["pk"])

            # If follow doesn't exist, create it
            if (len(Follow.objects.filter(profile=followed_profile, follower_profile=follower_profile)) == 0
            and followed_profile != follower_profile):
                Follow.objects.create(profile=followed_profile, follower_profile=follower_profile)

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
 
        # add followed profile into the context dictionary:
        user = self.request.user
        followed_profile = Profile.objects.get(pk=self.kwargs["pk"])
        if followed_profile == Profile.objects.get(user=user):
            context['own_profile'] = True
        context['followed_profile'] = followed_profile
        return context
    
class DeleteFollowView(LoginRequiredMixin, TemplateView):
    """A view to have the logged in user unfollow another user's profile."""

    template_name="mini_insta/delete_follow.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Accepts HTTP request and handles response logic."""

        user = self.request.user
        if user.is_authenticated:
            unfollower_profile = Profile.objects.get(user=user)
            unfollowed_profile = Profile.objects.get(pk=self.kwargs["pk"])

            # If follow exists, delete it
            if Follow.objects.filter(profile=unfollowed_profile, follower_profile=unfollower_profile).exists():
                follow = Follow.objects.get(profile=unfollowed_profile, follower_profile=unfollower_profile)
                follow.delete()

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
 
        # add unfollowed profile into the context dictionary:
        unfollowed_profile = Profile.objects.get(pk=self.kwargs["pk"])
        context['unfollowed_profile'] = unfollowed_profile
        return context

class LikePostView(LoginRequiredMixin, TemplateView):
    """A view to have the logged in user like another user's post."""

    template_name="mini_insta/like.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Accepts HTTP request and handles response logic."""

        user = self.request.user
        if user.is_authenticated:
            liker_profile = Profile.objects.get(user=user)

            liked_post = Post.objects.get(pk=self.kwargs["pk"])

            # If like doesn't exist, create it
            if (len(Like.objects.filter(profile=liker_profile, post=liked_post)) == 0
            and liker_profile!=liked_post.profile):
                Like.objects.create(profile=liker_profile, post=liked_post)

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
 
        # add liked post into the context dictionary:
        user = self.request.user
        liked_post = Post.objects.get(pk=self.kwargs["pk"])
        if liked_post.profile == Profile.objects.get(user=user):
            context['own_post'] = True
        context['liked_post'] = liked_post
        return context
    
class DeleteLikeView(LoginRequiredMixin, TemplateView):
    """A view to have the logged in user unlike another user's post."""

    template_name="mini_insta/delete_like.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Accepts HTTP request and handles response logic."""

        user = self.request.user
        if user.is_authenticated:
            liker_profile = Profile.objects.get(user=user)
            unliked_post = Post.objects.get(pk=self.kwargs["pk"])

            # If like exists, delete it
            if Like.objects.filter(profile=liker_profile, post=unliked_post).exists():
                like = Like.objects.get(profile=liker_profile, post=unliked_post)
                like.delete()

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
 
        # add unliked post into the context dictionary:
        unliked_post = Post.objects.get(pk=self.kwargs["pk"])
        context['unliked_post'] = unliked_post
        return context