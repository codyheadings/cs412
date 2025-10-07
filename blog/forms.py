from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    """A form to add an Article to the database."""

    class Meta:
        """Associaate this form with a model from the database"""
        model=Article
        # fields = ["author", "title", "text", "image_url"]
        fields = ["author", "title", "text", "image_file"]

class UpdateArticleForm(forms.ModelForm):
    '''A form to update an article to the database.'''
 
    class Meta:
        '''associate this form with the Article model.'''
        model = Article
        fields = ['title', 'text', ]

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Comment
        fields = ['author', 'text', ]