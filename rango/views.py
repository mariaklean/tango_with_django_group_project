from rango.models import Category, Restaurant, Review
from django.shortcuts import render
from rango.models import Page
from rango.forms import CategoryForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from urllib.parse import urlencode
from django.contrib.auth.models import User

from rango.forms import PageForm

from django.http import HttpResponse


def index(request):
    # conext_dir={'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    # return render(request, 'rango/index.html',context=conext_dir)
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    restaurant_list = Restaurant.objects.order_by('name')

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict = {'categories': category_list, 'pages': page_list}
    # Call the helper function to handle the cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # add restaurants to index page
    context_dict['restaurants'] = restaurant_list

    # Render the response and send it back!
    response = render(request, 'rango/index.html', context=context_dict)

    return response


def about(request):
    # return HttpResponse("Rango says here is the about page. <a href='http://127.0.0.1:8000/'>Index</a>")
    context_dict = {}
    context_dict['boldmessage'] = ' Maria'
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    return render(request, 'rango/about.html', context=context_dict)


def show_restaurant(request, restaurant_name_slug):
    context_dict = {}

    restaurant = Restaurant.objects.get(slug=restaurant_name_slug)
    location = restaurant.location
    print(restaurant.id)
    reviews = Review.objects.filter(restaurant__id=restaurant.id)
    for review in reviews:
        print(review.user)
        print(review.review)

    # build the url for google maps
    url_base = "https://maps.googleapis.com/maps/api/staticmap?"
    params = {
        'center': str(location.latitude)+','+str(location.longitude),
        'zoom': '16',
        'size': '500x400',
        'key': 'AIzaSyAbk3bAYXqPu8jSvHbBb-BBDfEbgBtiXJ8',
        'markers': 'color:red|'+str(location.latitude)+','+str(location.longitude),
    }

    encoded_params = urlencode(params)
    print(encoded_params)
    url = url_base+encoded_params
    context_dict['google_url'] = url


    try:
        context_dict['restaurant'] = restaurant
        context_dict['reviews'] = reviews
    except Restaurant.DoesNotExist:
        context_dict['restaurant'] = None
        context_dict['reviews'] = None

    return render(request, 'rango/show_restaurant.html', context=context_dict)




def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?

        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango/')

        else:
            # The supplied form contained errors
            # just print them to the terminal.
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None
    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug':
                                                    category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


@login_required
def browse(request):
    return render(request, 'rango/browse.html')


# Use the login_required() decorator to ensure only those logged in can
# access the view.

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(request.COOKIES.get('visits', '1'))
    print(visits)
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits
