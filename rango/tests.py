from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from rango.models import Restaurant, Review


class SigninTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


class RestaurantTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user2 = get_user_model().objects.create_user(username='test2', password='12test12', email='test2t@example.com')
        self.restaurant = Restaurant.objects.create(user=self.user, name='Test', rate=5.0, description='this is a test')

    def tearDown(self):
        self.restaurant.delete()

    def test_restaurant_created(self):
        res = Restaurant.objects.get(name='Test')
        self.assertEquals(res.name, 'Test')
        self.assertEquals(res.description, 'this is a test')
        self.assertNotEquals(res.rate, 0)

    def test_restaurant_is_with_user(self):
        res = Restaurant.objects.filter(name='Test')
        self.assertIn(self.restaurant, res)
        self.assertEquals(res[0].user.username, 'test')

    def test_restaurant_not_belong_user(self):
        res = Restaurant.objects.filter(user=self.user2)
        self.assertNotIn(self.restaurant, res)