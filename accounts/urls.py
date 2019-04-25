from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('restricted/', views.restricted_view, name="restricted"),
    path('', views.saved_products, name='index_accounts'),
    path('add_to_favourites', views.add_to_favourites, name="add_to_favourites"),
    path('saved_products', views.saved_products, name="saved_products"),
    path('user_info', views.user_info, name="user_info"),
    path('delete_all_users', views.delete_all_users, name="delete_all_users"),
]
