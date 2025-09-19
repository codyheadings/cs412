# file: restaurant/views.py
# author: Cody Headings, codyh@bu.edu, 9/16/2025
# desc: defintions for individual page views

from django.shortcuts import render
import random
import time

specials = [
    "Bab's Perfect Pork Belly",
    "Bab's Saucy Sliders",
    "Bab's Mountain of Mystery Meat",
    "Bab's Flamin' Ribs",
    "Bab's Slathered Steak",
    "Bab's Krispy Kebab",
    "Bab's Rotisserie Roast",
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
        special = request.POST.get("special", False)
        brisket = request.POST.get("brisket", False)
        chicken = request.POST.get("chicken", False)
        plain = request.POST.get("plain", False)
        extra_spice = request.POST.get("extra_spice", False)
        burger = request.POST.get("burger", False)
        cheddar = request.POST.get("cheddar", False)
        extra_patty = request.POST.get("extra_patty", False)
        bbq_bacon = request.POST.get("bbq_bacon", False)
        instructions = request.POST["instructions"]
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        readytime = time.ctime(time.time() + random.randint(1800,3600))
        price = 0
        if(special != False):
            price += 12.99
        if(brisket != False):
            price += 13.49
        if(chicken != False):
            price += 11.99
        if(extra_spice != False):
            price += 0.25
        if(burger != False):
            price += 10.99
        if(extra_patty != False):
            price += 1.99
        if(bbq_bacon != False):
            price += 1.49
        if(cheddar != False):
            price += 0.50


        # create context variables for use in template
        context = {
            "name": name,
            "phone": phone,
            "email": email,
            "instructions": instructions,
            "special": special,
            "brisket": brisket,
            "chicken": chicken,
            "plain": plain,
            "extra_spice": extra_spice,
            "burger": burger,
            "cheddar": cheddar,
            "extra_patty": extra_patty,
            "bbq_bacon": bbq_bacon,
            "readytime": readytime,
            "price": price
        }

    # default: return form to fill in if not submitting
    return render(request, template_name, context)