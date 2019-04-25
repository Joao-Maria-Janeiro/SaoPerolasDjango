from django.contrib import admin

# Register your models here.
from .models import Product, BackGroundImage

admin.site.register(Product)
admin.site.register(BackGroundImage)
