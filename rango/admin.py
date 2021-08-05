from rango.models import Restaurant, Review, Location, UserProfile, Category, Page
from django.contrib import admin


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')
    prepopulated_fields = {'slug': ('name',)}


class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Location)
admin.site.register(Review)
admin.site.register(UserProfile)