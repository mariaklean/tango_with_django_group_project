from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.
class Restaurant(models.Model):
    NAME_MAX_LENGTH = 250

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    rate = models.FloatField(default=0.0)
    description = models.TextField(max_length=1000, default='this is a description')
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Restaurant, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return self.name


class Review(models.Model):
    NAME_MAX_LENGTH = 500
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    review = models.TextField(max_length=NAME_MAX_LENGTH)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return str(self.rating)


class Location(models.Model):
    POSTCODE_MAX_LENGHT = 50
    CITY_MAX_LENGHT = 200
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    post_code = models.CharField(max_length=POSTCODE_MAX_LENGHT)
    city = models.CharField(max_length=CITY_MAX_LENGHT)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = 'Location'


class Category(models.Model):
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
