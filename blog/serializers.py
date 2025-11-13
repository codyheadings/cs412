# blog/serializers/py
# Convert our django data models to a text
# representation suitable to transmit over HTTP

from rest_framework import serializers
from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    """
    A serializer for the article model.
    Specify which model/fields to send in the API.
    """

    class Meta:
        model = Article
        fields = ["id", "title", "author", "text"]

    # add methods to customize the CRUD operatons
    def create(self, validated_data):
        """Override the superclass method that handles object creation."""
        print(f'articleSerializer.create, validated_data={validated_data}.')
        # # create an Article object
        # article = Article(**validated_data)
        # # attach FK to user
        # article.user = User.objects.first()
        # # save the object to the database
        # article.save()
        # # return an object instance
        # return article
    
        # alternate way:
        validated_data['user'] = User.objects.first()
        return Article.objects.create(**validated_data)
