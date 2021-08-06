import os
from typing import cast

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django

django.setup()
from rango.models import Restaurant, Review, Location
from django.contrib.auth.models import User


def populate():
    location = {
        'post_code': 'G207EW',
        'city': 'Glasgow',
        'latitude': 55.8806944,
        'longitude': -4.272544
    }

    location2 = {
        'post_code': 'G128QQ',
        'city': 'Glasgow',
        'latitude': 55.869203,
        'longitude': -4.2783827
    }

    location3 = {
        'post_code': 'G128EL',
        'city': 'Glasgow',
        'latitude': 55.8758768,
        'longitude': -4.2831564
    }

    reviews = [{
        'review': 'This restaurant is excellent',
        'rate': 5
        },
        {
            'review': 'One of the best restaurants I\'ve ever tried',
            'rate': 4
        }
    ]

    restaurant = {
        'Colombian paradise': {
            'name': 'Colombian paradise',
            'rate': 5.0,
            'location': location,
            'reviews': reviews,
            'description': 'Colombian food for everyone'
        },
        'Mac Tassos': {
            'name': 'Mac Tassos',
            'rate': 4.9,
            'location': location2,
            'reviews': reviews,
            'description': 'The best gyros and greek food you can eat'
        },
        'Brgr': {
            'name': 'Brgr',
            'rate': 4.9,
            'location': location3,
            'reviews': reviews,
            'description': 'Burgers for all kind of people'
        }
    }

    user = User.objects.create_user('test1', 'test1@hotmail.com', "test1234")

    for res, res_data in restaurant.items():
        r = add_restaurant(user, res_data['name'], res_data['rate'], res_data['description'])
        l = add_location(r, res_data['location']['post_code'], res_data['location']['city'],
                         res_data['location']['latitude'], res_data['location']['longitude'])
        for rev in res_data['reviews']:
            review = add_review(user, r, rev['review'], rev['rate'])


def add_location(restaurant, post_code, city, latitude, longitude):
    l = Location.objects.get_or_create(restaurant=restaurant, post_code=post_code)[0]
    l.city = city
    l.latitude = latitude
    l.longitude = longitude

    l.save()
    return l


def add_restaurant(user, name, rate, description):
    r = Restaurant.objects.get_or_create(user=user, name=name)[0]
    r.rate = rate
    r.description = description

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
