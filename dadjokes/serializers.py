# file: dadjokes/models.py
# author: Cody Headings, codyh@bu.edu, 11/13/2025
# desc: convert django data models to text for transport over HTTP
from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    """
    A serializer for the joke model.
    Specify which model/fields to send in the API.
    """

    class Meta:
        model = Joke
        fields = ["text", "name", "timestamp"]

class PictureSerializer(serializers.ModelSerializer):
    """
    A serializer for the Picture model.
    Specify which model/fields to send in the API.
    """

    class Meta:
        model = Picture
        fields = ["image_url", "name", "timestamp"]