# file: quotes/views.py
# author: Cody Headings, codyh@bu.edu, 9/9/2025
# desc: defintions for individual page views

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Global lists of quotes and image urls
quote_list = [
    "1",
    "2",
    "3",
]

image_list = [
    "url1",
    "url2",
    "url3",
]

# Create your views here.
def quote(request):
    """Respond to the URL 'quote' and '', delegate work to a template."""

    template_name = 'quotes/quote.html'
    quote_number = random.randint(0,len(quote_list))
    image_number = random.randint(0,len(image_list))

    # a dict of context variables (key value pairs)
    context = {
        'quote' : quote_list[quote_number],
        'image' : image_list[image_number],
    }
    return render(request, template_name, context)

def about(request):
    """Respond to the URL 'about', delegate work to a template."""

    template_name = 'quotes/about.html'

    # a dict of context variables (key value pairs)
    context = {

    }
    return render(request, template_name, context)

def show_all(request):
    """Respond to the URL 'show_all', delegate work to a template."""

    template_name = 'quotes/show_all.html'

    # a dict of context variables (key value pairs)
    context = {
        'quotes' : quote_list,
        'images' : image_list
    }
    return render(request, template_name, context)