# file: restaurant/views.py
# author: Cody Headings, codyh@bu.edu, 9/16/2025
# desc: defintions for individual page views

from django.shortcuts import render
import random

specials = [
    "",
    "",
    "",
    "",
]

# Create your views here.
def main(request):
    """Respond to the URL 'main' and '', delegate work to a template."""

    template_name = 'restaurant/main.html'

    # a dict of context variables (key value pairs)
    return render(request, template_name)

def order(request):
    """Show the order form to the user."""

    template_name = 'restaurant/order.html'
    daily_number = random.randint(1,len(specials))-1

    # a dict of context variables (key value pairs)
    context = {
        'daily_special' : specials[daily_number],
    }

    return render(request, template_name, context)

def confirmation(request):
    """Process the form submission and generate a result."""

    template_name = "restaurant/confirmation.html"
    print(request.POST)

    #check if POST data was sent with the HTTP POST message:
    if request.POST:

        # extract form fields into variables
        

        # create context variables for use in template
        context = {

        }

    # default: return form to fill in if not submitting
    return render(request, template_name, context)