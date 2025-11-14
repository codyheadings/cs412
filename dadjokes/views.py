# file: dadjokes/views.py
# author: Cody Headings, codyh@bu.edu, 11/13/2025
# desc: view functions to return html renders

import random
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from dadjokes.models import *

# Create your views here.
class RandomView(DetailView):
    """Display a single joke and picture both selected at random."""

    model = Joke
    template_name = "dadjokes/random.html"
    context_object_name = "joke"

    # methods
    def get_object(self):
        """return one instance of random joke"""
        all_jokes = Joke.objects.all()
        joke = random.choice(all_jokes)
        return joke
    
    def get_context_data(self, **kwargs):
        '''Return dictionary of context variables for use in template.'''
        # calling the superclass method
        context = super().get_context_data()

        # add random image url to context data:
        all_pics = Picture.objects.all()
        picture = random.choice(all_pics)
        context['picture'] = picture.image_url

        return context
    
class JokeListView(ListView):
    '''Create a subclass of ListView to display all jokes.'''
    
    model = Joke
    template_name = 'dadjokes/show_all_jokes.html'
    context_object_name = 'jokes'

class PictureListView(ListView):
    '''Create a subclass of ListView to display all pictures.'''
    
    model = Picture
    template_name = 'dadjokes/show_all_pictures.html'
    context_object_name = 'pictures'

class JokeDetailView(DetailView):
    '''Create a subclass of DetailView to display a single joke.'''
    
    model = Joke
    template_name = 'dadjokes/show_joke.html'
    context_object_name = 'joke'

class PictureDetailView(DetailView):
    '''Create a subclass of DetailView to display a single picture.'''
    
    model = Picture
    template_name = 'dadjokes/show_picture.html'
    context_object_name = 'picture'

# REST API:
from rest_framework import generics
from .serializers import *

class JokeListAPIView(generics.ListCreateAPIView):
    """
    An API view to return a listing of Jokes
    and create a Joke.
    """

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class RandomJokeAPIView(generics.RetrieveAPIView):
    """
    An API view to return a random Joke.
    """

    def get_object(self):
        return random.choice(Joke.objects.all())
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListAPIView):
    """
    An API view to return a listing of Pictures.
    """

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomPictureAPIView(generics.RetrieveAPIView):
    """
    An API view to return a random Picture.
    """

    def get_object(self):
        return random.choice(Picture.objects.all())
    serializer_class = PictureSerializer