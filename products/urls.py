from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('products/colares/colar<int:id>/', views.colares, name='colares'),
    path('products/pulseiras/', views.pulseiras, name='index_pulseira'),
    path('products/pulseiras/pulseira<int:id>/', views.pulseira_individual, name='pulseira_individual'),
    path('contactos', views.contactos, name='contactos'),
    path('products/brincos/', views.brincos, name='index_brincos'),
    path('products/brincos/brinco<int:id>/', views.brinco_individual, name='brinco_individual'),
    path('products/create', views.product_create, name="create_product"),
]
