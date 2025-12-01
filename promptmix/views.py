# file: promptmix/views.py
# author: Cody Headings, codyh@bu.edu, 11/25/2025
# desc: view functions to return html renders

from promptmix.forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.
class ProfileDetailView(DetailView):
    """Subclass of DetailView to display a single profile page."""
    
    model = Profile
    template_name = 'promptmix/show_profile.html'
    context_object_name = 'profile'

class PromptDetailView(DetailView):
    """Subclass of DetailView to display a single prompt page."""
    
    model = Prompt
    template_name = 'promptmix/show_prompt.html'
    context_object_name = 'prompt'

class CreatePromptView(CreateView):
    '''A view to create a new prompt and save it to the database.'''
 
    form_class = CreatePromptForm
    template_name = "promptmix/create_prompt_form.html"

    # def get_object(self):
    #     """Override default method to get object from current user."""

    #     # find the logged in user
    #     user = self.request.user

    #     profile = Profile.objects.get(user=user)

    #     return profile

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data()
 
        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
 
        # add this profile into the context dictionary:
        context['profile'] = profile
        return context
 
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        Adds the foreign key (of the Profile) to the Prompt
        object before saving it to the database.
        '''
 
		# instrument our code to display form fields: 
        print(f"CreatePromptView.form_valid: cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this profile to the prompt
        form.instance.profile = profile # set the FK
 
        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirects to new prompt page after successful creation."""
        return reverse('show_prompt', kwargs={'pk':self.object.pk})
    
class CreateRemixView(CreateView):
    '''A view to create a new Remix and save it to the database.'''
 
    form_class = CreateRemixForm
    template_name = "promptmix/create_remix_form.html"

    def dispatch(self, request, *args, **kwargs):
        """Determine whether user is remixing a prompt or another remix."""
        
        self.prompt = None
        self.remix = None

        if "prompt_id" in kwargs:
            self.prompt = Prompt.objects.get(pk=kwargs["prompt_id"])

        if "remix_id" in kwargs:
            self.remix = Remix.objects.get(pk=kwargs["remix_id"])
            self.prompt = self.remix.prompt

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Add all other fields not entered by user in the form."""
        remix = form.save(commit=False)
        remix.profile = Profile.objects.first()
        remix.prompt = self.prompt
        remix.remix = self.remix
        remix.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirects to new prompt page after successful creation."""
        return reverse('show_prompt', kwargs={'pk':self.prompt.pk})
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data(**kwargs)
        context["prompt"] = self.prompt
        context["parent"] = self.remix
        return context
    
# class UpdateProfileView(LoginRequiredMixin, UpdateView):
#     """View class to handle update of a profile based on its pk."""

#     model = Profile
#     form_class = UpdateProfileForm
#     template_name = "promptmix/update_profile_form.html"

#     def get_object(self):
#         """Override default method to get object from current user."""

#         # find the logged in user
#         user = self.request.user

#         profile = Profile.objects.get(user=user)

#         return profile

#     def get_login_url(self) -> str:
#         '''return the URL required for login'''
#         return reverse('login')

# class DeletePromptView(LoginRequiredMixin, DeleteView):
#     '''A view to delete a Prompt and remove it from the database.'''
 
#     template_name = "promptmix/delete_prompt_form.html"
#     model = Prompt
#     context_object_name = 'prompt'

#     def get_login_url(self) -> str:
#         '''return the URL required for login'''
#         return reverse('login')

#     def get_context_data(self, **kwargs):
#         """Provides context data to the delet prompt form."""

#         # calling the superclass method
#         context = super().get_context_data(**kwargs)
#         # get current prompt object
#         prompt = self.object
#         profile = prompt.profile
 
#         # add this profile into the context dictionary:
#         context['profile'] = profile
#         context['prompt'] = prompt
#         return context

#     def get_success_url(self):
#         """Return url to redirect to after delete."""

#         # get the pk for this prompt
#         pk = self.kwargs.get('pk')
#         prompt = Prompt.objects.get(pk=pk)
        
#         # find the profile to which this Prompt is related by FK
#         profile = prompt.profile
        
#         # reverse to show the profile page
#         return reverse('show_profile', kwargs={'pk':profile.pk})

# class PromptFeedListView(ListView):
#     """Create a subclass of ListView to display prompt feed for a profile."""
    
#     model = Prompt
#     template_name = 'promptmix/show_feed.html'
#     context_object_name = 'prompts'

#     def get_object(self):
#         """Override default method to get object from current user."""

#         # find the logged in user
#         user = self.request.user

#         profile = Profile.objects.get(user=user)

#         return profile

#     def get_queryset(self):
#         """Return the feed prompts from followed profiles."""
#         profile = Profile.objects.get(user=self.request.user)
#         return profile.get_prompt_feed()

#     def get_context_data(self, **kwargs):
#         """Add the profile object to the context data."""
#         context = super().get_context_data(**kwargs)

#         profile = self.get_object()

#         context['profile'] = profile
#         return context
    
# class CreateProfileView(CreateView):
#     """A view to create a new profile and save it to the database."""

#     form_class = CreateProfileForm
#     template_name = "promptmix/create_profile_form.html"

#     def get_context_data(self):
#         '''Return the dictionary of context variables for use in the template.'''
#         context = super().get_context_data()
 
#         # add UserCreationForm into the context dictionary:
#         context['user_form'] = UserCreationForm
#         return context
    
#     def form_valid(self, form):
#         '''Handles the form submission and saves the 
#         new object to the Django database.
#         '''

#         print(f"CreateProfileView.form_valid: cleaned_data={form.cleaned_data}")
        
#         user_form = UserCreationForm(self.request.POST)
#         user = user_form.save()

#         login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
 
#         form.instance.user = user

#         # delegate to the superclass method form_valid:
#         return super().form_valid(form)
    
# class DeleteFollowView(LoginRequiredMixin, TemplateView):
#     """A view to have the logged in user unfollow another user's profile."""

#     template_name="promptmix/delete_follow.html"

#     def get_login_url(self) -> str:
#         '''return the URL required for login'''
#         return reverse('login')

#     def dispatch(self, request, *args, **kwargs):
#         """Accepts HTTP request and handles response logic."""

#         user = self.request.user
#         if user.is_authenticated:
#             unfollower_profile = Profile.objects.get(user=user)
#             unfollowed_profile = Profile.objects.get(pk=self.kwargs["pk"])

#             # If follow exists, delete it
#             if Follow.objects.filter(profile=unfollowed_profile, follower_profile=unfollower_profile).exists():
#                 follow = Follow.objects.get(profile=unfollowed_profile, follower_profile=unfollower_profile)
#                 follow.delete()

#         return super().dispatch(request, *args, **kwargs)
    
#     def get_context_data(self, **kwargs):
#         '''Return the dictionary of context variables for use in the template.'''
#         context = super().get_context_data()
 
#         # add unfollowed profile into the context dictionary:
#         unfollowed_profile = Profile.objects.get(pk=self.kwargs["pk"])
#         context['unfollowed_profile'] = unfollowed_profile
#         return context

# class BoostPromptView(LoginRequiredMixin, TemplateView):
#     """A view to have the logged in user boost another user's prompt."""

#     template_name="promptmix/boost.html"

#     def get_login_url(self) -> str:
#         '''return the URL required for login'''
#         return reverse('login')

#     def dispatch(self, request, *args, **kwargs):
#         """Accepts HTTP request and handles response logic."""

#         user = self.request.user
#         if user.is_authenticated:
#             booster_profile = Profile.objects.get(user=user)

#             boosted_prompt = Prompt.objects.get(pk=self.kwargs["pk"])

#             # If like doesn't exist, create it
#             if (len(Boost.objects.filter(profile=booster_profile, prompt=boosted_prompt)) == 0
#             and booster_profile!=boosted_prompt.profile):
#                 Boost.objects.create(profile=booster_profile, prompt=boosted_prompt)

#         return super().dispatch(request, *args, **kwargs)
    
#     def get_context_data(self, **kwargs):
#         '''Return the dictionary of context variables for use in the template.'''
#         context = super().get_context_data()
 
#         # add boosted prompt into the context dictionary:
#         user = self.request.user
#         boosted_prompt = Prompt.objects.get(pk=self.kwargs["pk"])
#         if boosted_prompt.profile == Profile.objects.get(user=user):
#             context['own_prompt'] = True
#         context['boosted_prompt'] = boosted_prompt
#         return context
    
# class DeleteBoostView(LoginRequiredMixin, TemplateView):
#     """A view to have the logged in user unlike another user's prompt."""

#     template_name="promptmix/delete_like.html"

#     def get_login_url(self) -> str:
#         '''return the URL required for login'''
#         return reverse('login')

#     def dispatch(self, request, *args, **kwargs):
#         """Accepts HTTP request and handles response logic."""

#         user = self.request.user
#         if user.is_authenticated:
#             booster_profile = Profile.objects.get(user=user)
#             unboosted_prompt = Prompt.objects.get(pk=self.kwargs["pk"])

#             # If like exists, delete it
#             if Boost.objects.filter(profile=booster_profile, prompt=unboosted_prompt).exists():
#                 like = Boost.objects.get(profile=booster_profile, prompt=unboosted_prompt)
#                 like.delete()

#         return super().dispatch(request, *args, **kwargs)
    
#     def get_context_data(self, **kwargs):
#         '''Return the dictionary of context variables for use in the template.'''
#         context = super().get_context_data()
 
#         # add unboosted prompt into the context dictionary:
#         unboosted_prompt = Prompt.objects.get(pk=self.kwargs["pk"])
#         context['unboosted_prompt'] = unboosted_prompt
#         return context