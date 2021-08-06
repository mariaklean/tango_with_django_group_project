from rango.models import Restaurant, Review, Location, UserProfile, Category, Page
from django.contrib import admin


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')
    prepopulated_fields = {'slug': ('name',)}


class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rating', 'restaurant', 'user')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Location)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile)