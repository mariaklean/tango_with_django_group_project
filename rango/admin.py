from rango.models import Restaurant, Review, Location, UserProfile
from django.contrib import admin


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')
    prepopulated_fields = {'slug': ('name',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rating', 'restaurant', 'user')


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Location)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile)
