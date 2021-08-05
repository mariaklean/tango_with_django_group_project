import os
from typing import cast

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django

django.setup()
from rango.models import Restaurant, Review, Location
from django.contrib.auth.models import User


def populate():
    location = {
        'post_code': 'G20 7EW',
        'city': 'Glasgow',
        'latitude': 55.8806944,
        'longitude': -4.272544
    }

    reviews = [{
        'review': 'This restaurant is excellent',
        'rate': 5
    }]

    restaurant = {
        'Colombian paradise':{
        'name': 'Colombian paradise',
        'rate': 5.0,
        'location': location,
        'reviews': reviews
        }
    }

    user = User.objects.get_by_natural_key('david')

    for res, res_data in restaurant.items():
        r = add_restaurant(user, res_data['name'], res_data['rate'])
        l = add_location(r, res_data['location']['post_code'], res_data['location']['city'], res_data['location']['latitude'], res_data['location']['longitude'])
        for rev in res_data['reviews']:
            review = add_review(user, r, rev['review'], rev['rate'])


def add_location(restaurant, post_code, city, latitude, longitude):
    l = Location.objects.get_or_create(restaurant=restaurant, post_code=post_code)[0]
    l.city = city
    l.latitude = latitude
    l.longitude = longitude

    l.save()
    return l


def add_restaurant(user, name, rate):
    r = Restaurant.objects.get_or_create(user=user, name=name)[0]
    r.rate = rate

    r.save()
    return r


def add_review(user, restaurant, review, rate):
    rev = Review.objects.get_or_create(user=user, restaurant=restaurant)[0]
    rev.review = review
    rev.rating = rate

    rev.save()
    return rev


if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
