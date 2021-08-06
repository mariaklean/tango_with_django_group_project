from rango.models import Restaurant, Review
from django.shortcuts import render
from rango.forms import ReviewForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from urllib.parse import urlencode


def index(request):

    restaurant_list = Restaurant.objects.order_by('name')

    context_dict = {}
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

    user = None
    if request.user.is_authenticated:
        user = request.user

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
        'size': '600x400',
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

    # add form to create new comments

    try:
        restaurant = Restaurant.objects.get(slug=restaurant_name_slug)
    except:
        restaurant = None

    if restaurant is None:
        return redirect('/rango/')

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            if restaurant:
                review = form.save(commit=False)
                review.restaurant = restaurant
                review.user = user
                review.save()

                return redirect(reverse('rango:show_restaurant',
                                        kwargs={'restaurant_name_slug':
                                                    restaurant_name_slug}))
        else:
            print(form.errors)

    context_dict['form'] = form
    context_dict['restaurant'] = restaurant

    return render(request, 'rango/show_restaurant.html', context=context_dict)


@login_required
def browse(request):
    context_dict = {}
    restaurants = Restaurant.objects.all()
    context_dict['restaurants'] = restaurants

    return render(request, 'rango/browse.html', context=context_dict)


@login_required
def my_account(request):
     return render(request, 'rango/my_account.html')

    



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
