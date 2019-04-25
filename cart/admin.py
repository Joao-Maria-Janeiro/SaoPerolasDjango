from django.contrib import admin
from .models import Cart, Cart_userless, CartProduct, ShippingDetails, Order, OrderUserless

# Register your models here.
admin.site.register(Cart)
admin.site.register(Cart_userless)
admin.site.register(CartProduct)
admin.site.register(ShippingDetails)
admin.site.register(Order)
admin.site.register(OrderUserless)
