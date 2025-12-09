# file: promptmix/views.py
# author: Cody Headings, codyh@bu.edu, 11/25/2025
# desc: view functions to return html renders

from promptmix.forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q, Count
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

    def get_context_data(self, **kwargs):
        """Add the profile object to the context data."""
        context = super().get_context_data(**kwargs)
        context["get_request"] = self.request.GET

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        prompts = profile.get_all_prompts()

        if 'keywords' in self.request.GET:
            keywords = self.request.GET['keywords']
            if keywords:
                prompts = prompts.filter(Q(subject__icontains=keywords) | Q(text__icontains=keywords))

        prompts = prompts.annotate(boost_count=Count('boosted_prompt',
                                                      distinct=True))

        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort=="newest":
                prompts = prompts.order_by('-timestamp')
            elif sort=="oldest":
                prompts = prompts.order_by('timestamp')
            elif sort=="unpopular":
                prompts = prompts.order_by('boost_count', '-timestamp')
            else:
                # sort by most popular
                prompts = prompts.order_by('-boost_count', '-timestamp')

        user = self.request.user
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
        else:
            profile = None

        prompt_boosts = Boost.objects.filter(profile=profile, remix__isnull=True)
        remix_boosts = Boost.objects.filter(profile=profile, prompt__isnull=True)
        follows = Follow.objects.filter(follower_profile=profile)

        boosted_prompts = list(Prompt.objects.none())
        boosted_remixes = list(Remix.objects.none())
        followed_prompts = list(Prompt.objects.none())

        for boost in prompt_boosts:
            boosted_prompts += [boost.prompt]

        for boost in remix_boosts:
            boosted_remixes += [boost.remix]

        for follow in follows:
            followed_prompts += [follow.prompt]

        context["get_request"] = self.request.GET
        if boosted_prompts:
            context["boosted_prompts"] = boosted_prompts
        if boosted_remixes:
            context["boosted_remixes"] = boosted_remixes
        if followed_prompts:
            context["followed_prompts"] = followed_prompts   

        context["prompts"] = prompts

        return context

class PromptDetailView(DetailView):
    """Subclass of DetailView to display a single prompt page."""
    
    model = Prompt
    template_name = 'promptmix/show_prompt.html'
    context_object_name = 'prompt'

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data()

        # find the logged in user
        user = self.request.user
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
        else:
            profile = None

        prompt_boosts = Boost.objects.filter(profile=profile, remix__isnull=True)
        remix_boosts = Boost.objects.filter(profile=profile, prompt__isnull=True)
        follows = Follow.objects.filter(follower_profile=profile)

        boosted_prompts = list(Prompt.objects.none())
        boosted_remixes = list(Remix.objects.none())
        followed_prompts = list(Prompt.objects.none())

        for boost in prompt_boosts:
            boosted_prompts += [boost.prompt]

        for boost in remix_boosts:
            boosted_remixes += [boost.remix]

        for follow in follows:
            followed_prompts += [follow.prompt]

        context['profile'] = profile
        context["get_request"] = self.request.GET
        if boosted_prompts:
            context["boosted_prompts"] = boosted_prompts
        if boosted_remixes:
            context["boosted_remixes"] = boosted_remixes
        if followed_prompts:
            context["followed_prompts"] = followed_prompts   
 
        context['prompt_page'] = "TRUE"
        return context

class CreatePromptView(LoginRequiredMixin, CreateView):
    '''A view to create a new prompt and save it to the database.'''
 
    form_class = CreatePromptForm
    template_name = "promptmix/create_prompt_form.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_object(self):
        """Override default method to get object from current user."""

        # find the logged in user
        user = self.request.user

        profile = Profile.objects.get(user=user)

        return profile

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        # calling the superclass method
        context = super().get_context_data()
 
        # find/add the profile to the context data
        profile = self.get_object()
 
        # add this profile into the context dictionary:
        context['profile'] = profile
        return context
 
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        Adds the foreign key (of the Profile) to the Prompt
        object before saving it to the database.
        '''

        profile = self.get_object()
        # attach this profile to the prompt
        prompt = form.save(commit=False)
        prompt.profile = profile
        prompt.save()

        Boost.objects.get_or_create(profile=profile, prompt=prompt)
 
        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirects to new prompt page after successful creation."""
        return reverse('show_prompt', kwargs={'pk':self.object.pk})
    
class CreateRemixView(LoginRequiredMixin, CreateView):
    '''A view to create a new Remix and save it to the database.'''
 
    form_class = CreateRemixForm
    template_name = "promptmix/create_remix_form.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Determine whether user is remixing a prompt or another remix."""

        if "prompt_id" in kwargs:
            self.prompt = Prompt.objects.get(pk=kwargs["prompt_id"])
            self.remix = None

        if "remix_id" in kwargs:
            self.remix = Remix.objects.get(pk=kwargs["remix_id"])
            self.prompt = Prompt.objects.get(pk=self.remix.prompt.pk)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Add all other fields not entered by user in the form."""
        remix = form.save(commit=False)
        user = self.request.user
        profile = Profile.objects.get(user=user)
        remix.profile = profile
        remix.prompt = self.prompt
        remix.remix = self.remix
        remix.save()

        Boost.objects.get_or_create(profile=profile, remix=remix)

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
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """View class to handle update of a profile based on its pk."""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "promptmix/update_profile_form.html"

    def get_object(self):
        """Override default method to get object from current user."""

        # find the logged in user
        user = self.request.user

        profile = Profile.objects.get(user=user)

        return profile

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
class UpdateRemixView(LoginRequiredMixin, UpdateView):
    """View class to handle update of a remix based on its pk."""

    model = Remix
    form_class = UpdateRemixForm
    template_name = "promptmix/update_remix_form.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
class UpdatePromptView(LoginRequiredMixin, UpdateView):
    """View class to handle update of a prompt based on its pk."""

    model = Prompt
    form_class = UpdatePromptForm
    template_name = "promptmix/update_prompt_form.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

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

class PromptFeedListView(ListView):
    """Create a subclass of ListView to display prompt feed for a profile."""
    
    model = Prompt
    template_name = 'promptmix/show_feed.html'
    context_object_name = 'prompts'
    paginate_by = 5

    def get_object(self):
        """Override default method to get object from current user."""

        # find the logged in user
        user = self.request.user

        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
        else:
            profile = None

        return profile

    def get_queryset(self):
        """Return the feed prompts from the database."""
        prompts = super().get_queryset()

        if 'keywords' in self.request.GET:
            keywords = self.request.GET['keywords']
            if keywords:
                prompts = prompts.filter(Q(subject__icontains=keywords) 
                                         | Q(text__icontains=keywords))

        prompts = prompts.annotate(boost_count=Count('boosted_prompt',
                                                      distinct=True))

        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort=="newest":
                prompts = prompts.order_by('-timestamp')
            elif sort=="oldest":
                prompts = prompts.order_by('timestamp')
            elif sort=="unpopular":
                prompts = prompts.order_by('boost_count', '-timestamp')
            else:
                # sort by most popular
                prompts = prompts.order_by('-boost_count', '-timestamp')

        return prompts

    def get_context_data(self, **kwargs):
        """Add the profile object to the context data."""
        context = super().get_context_data(**kwargs)

        profile = self.get_object()

        prompt_boosts = Boost.objects.filter(profile=profile, remix__isnull=True)
        remix_boosts = Boost.objects.filter(profile=profile, prompt__isnull=True)
        follows = Follow.objects.filter(follower_profile=profile)

        boosted_prompts = list(Prompt.objects.none())
        boosted_remixes = list(Remix.objects.none())
        followed_prompts = list(Prompt.objects.none())

        for boost in prompt_boosts:
            boosted_prompts += [boost.prompt]

        for boost in remix_boosts:
            boosted_remixes += [boost.remix]

        for follow in follows:
            followed_prompts += [follow.prompt]

        context['profile'] = profile
        context["get_request"] = self.request.GET
        if boosted_prompts:
            context["boosted_prompts"] = boosted_prompts
        if boosted_remixes:
            context["boosted_remixes"] = boosted_remixes
        if followed_prompts:
            context["followed_prompts"] = followed_prompts   
        return context
    
class FollowedPromptsListView(LoginRequiredMixin, ListView):
    """Create a subclass of ListView to display all followed prompts for a profile."""
    
    model = Prompt
    template_name = 'promptmix/show_followed.html'
    context_object_name = 'prompts'
    paginate_by = 5

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_queryset(self):
        """Return the followed prompts from the database."""
        prompts = super().get_queryset()

        user = self.request.user
        profile = Profile.objects.get(user=user)

        prompts = prompts.filter(follow__follower_profile=profile)

        if 'keywords' in self.request.GET:
            keywords = self.request.GET['keywords']
            if keywords:
                prompts = prompts.filter(Q(subject__icontains=keywords) 
                                         | Q(text__icontains=keywords))

        prompts = prompts.annotate(boost_count=Count('boosted_prompt',
                                                      distinct=True))

        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort=="newest":
                prompts = prompts.order_by('-timestamp')
            elif sort=="oldest":
                prompts = prompts.order_by('timestamp')
            elif sort=="unpopular":
                prompts = prompts.order_by('boost_count', '-timestamp')
            else:
                # sort by most popular
                prompts = prompts.order_by('-boost_count', '-timestamp')

        return prompts

    def get_context_data(self, **kwargs):
        """Add the profile object to the context data."""
        context = super().get_context_data(**kwargs)

        user = self.request.user
        profile = Profile.objects.get(user=user)

        prompt_boosts = Boost.objects.filter(profile=profile, remix__isnull=True)
        remix_boosts = Boost.objects.filter(profile=profile, prompt__isnull=True)

        boosted_prompts = list(Prompt.objects.none())
        boosted_remixes = list(Remix.objects.none())

        for boost in prompt_boosts:
            boosted_prompts += [boost.prompt]

        for boost in remix_boosts:
            boosted_remixes += [boost.remix]

        context['profile'] = profile
        context["get_request"] = self.request.GET
        if boosted_prompts:
            context["boosted_prompts"] = boosted_prompts
        if boosted_remixes:
            context["boosted_remixes"] = boosted_remixes   
        return context
    
class CreateProfileView(CreateView):
    """A view to create a new profile and save it to the database."""

    form_class = CreateProfileForm
    template_name = "promptmix/create_profile_form.html"

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
    
class CreateFollowView(LoginRequiredMixin, TemplateView):
    """A view to have the logged in user follow a prompt."""

    template_name="promptmix/create_follow.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        """Accepts HTTP request and handles response logic."""

        user = self.request.user
        if user.is_authenticated:
            follower_profile = Profile.objects.get(user=user)

            followed_prompt = Prompt.objects.get(pk=self.kwargs["pk"])

            # If follow doesn't exist, create it
            if len(Follow.objects.filter(follower_profile=follower_profile, prompt=followed_prompt)) == 0:
                Follow.objects.create(follower_profile=follower_profile, prompt=followed_prompt)

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
 
        user = self.request.user
        profile = Profile.objects.get(user=user)
        context['profile'] = profile

        # add followed prompt into the context dictionary:
        followed_prompt = Prompt.objects.get(pk=self.kwargs["pk"])
        context['followed_prompt'] = followed_prompt
        return context
    
class DeleteFollowView(LoginRequiredMixin, TemplateView):
    """A view to have the logged in user unfollow a user's prompt."""

    template_name="promptmix/delete_follow.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Accepts HTTP request and handles response logic."""

        user = self.request.user
        if user.is_authenticated:
            unfollower_profile = Profile.objects.get(user=user)
            unfollowed_prompt = Prompt.objects.get(pk=self.kwargs["pk"])

            # If follow exists, delete it
            if Follow.objects.filter(follower_profile=unfollower_profile, prompt=unfollowed_prompt).exists():
                follow = Follow.objects.get(follower_profile=unfollower_profile, prompt=unfollowed_prompt)
                follow.delete()

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()

        user = self.request.user
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
 
        # add unfollowed profile into the context dictionary:
        unfollowed_prompt = Prompt.objects.get(pk=self.kwargs["pk"])
        context['unfollowed_prompt'] = unfollowed_prompt
        return context

class BoostPromptView(LoginRequiredMixin, TemplateView):
    """A view to have the logged in user boost another user's prompt."""

    template_name="promptmix/create_prompt_boost.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Accepts HTTP request and handles response logic."""

        user = self.request.user
        if user.is_authenticated:
            booster_profile = Profile.objects.get(user=user)

            boosted_prompt = Prompt.objects.get(pk=self.kwargs["pk"])

            # If boost doesn't exist, create it
            if len(Boost.objects.filter(profile=booster_profile, prompt=boosted_prompt)) == 0:
                Boost.objects.create(profile=booster_profile, prompt=boosted_prompt)

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()

        user = self.request.user
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
        
        # add boosted prompt into the context dictionary:
        boosted_prompt = Prompt.objects.get(pk=self.kwargs["pk"])
        context['boosted_prompt'] = boosted_prompt
        return context
    
class DeletePromptBoostView(LoginRequiredMixin, TemplateView):
    """A view to have the logged in user unlike another user's prompt."""

    template_name="promptmix/delete_boost.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Accepts HTTP request and handles response logic."""

        user = self.request.user
        if user.is_authenticated:
            booster_profile = Profile.objects.get(user=user)
            unboosted_prompt = Prompt.objects.get(pk=self.kwargs["pk"])

            # If like exists, delete it
            if Boost.objects.filter(profile=booster_profile, prompt=unboosted_prompt).exists():
                like = Boost.objects.get(profile=booster_profile, prompt=unboosted_prompt)
                like.delete()

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()

        user = self.request.user
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
 
        # add unboosted prompt into the context dictionary:
        unboosted_prompt = Prompt.objects.get(pk=self.kwargs["pk"])
        context['unboosted_prompt'] = unboosted_prompt
        return context
    
class BoostRemixView(LoginRequiredMixin, TemplateView):
    """A view to have the logged in user boost a user's remix."""

    template_name="promptmix/create_remix_boost.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Accepts HTTP request and handles response logic."""

        user = self.request.user
        if user.is_authenticated:
            booster_profile = Profile.objects.get(user=user)

            boosted_remix = Remix.objects.get(pk=self.kwargs["pk"])

            # If boost doesn't exist, create it
            if len(Boost.objects.filter(profile=booster_profile, remix=boosted_remix)) == 0:
                Boost.objects.create(profile=booster_profile, remix=boosted_remix)

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()

        user = self.request.user
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
 
        # add boosted remix into the context dictionary:
        boosted_remix = Remix.objects.get(pk=self.kwargs["pk"])
        context['boosted_remix'] = boosted_remix
        return context
    
class DeleteRemixBoostView(LoginRequiredMixin, TemplateView):
    """A view to have the logged in user unlike a user's remix."""

    template_name="promptmix/delete_boost.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """Accepts HTTP request and handles response logic."""

        user = self.request.user
        if user.is_authenticated:
            booster_profile = Profile.objects.get(user=user)
            unboosted_remix = Remix.objects.get(pk=self.kwargs["pk"])

            # If like exists, delete it
            if Boost.objects.filter(profile=booster_profile, remix=unboosted_remix).exists():
                like = Boost.objects.get(profile=booster_profile, remix=unboosted_remix)
                like.delete()

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()

        user = self.request.user
        profile = Profile.objects.get(user=user)
        context['profile'] = profile
 
        # add unboosted remix into the context dictionary:
        unboosted_remix = Remix.objects.get(pk=self.kwargs["pk"])
        context['unboosted_remix'] = unboosted_remix
        return context