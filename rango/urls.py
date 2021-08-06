from django.urls import path
from rango import views

app_name ='rango'

urlpatterns=[
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('browse/', views.browse, name='browse'),
    path('restaurant/<slug:restaurant_name_slug>', views.show_restaurant, name='show_restaurant'),
    path('my_account/', views.my_account , name='my_account'),

]