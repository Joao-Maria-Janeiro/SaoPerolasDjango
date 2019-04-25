from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('add/product<int:id>', views.add_to_cart, name="add_to_cart"),
    path('remove/product<int:id>', views.remove_from_cart, name="remove_from_cart"),
    path('increase/product<int:id>', views.increase_quantity,name="increase_quantity"),
    path('display/', views.display_cart, name="display_cart"),
    path('handler/', views.shipping_details, name="shipping_details"),
    path('details/', views.order_details, name="order_details"),
    path('', views.display_cart, name="index-cart"),
]
