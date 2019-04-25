from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from products.models import Product
from cart.models import ShippingDetails

# Create your models here.
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favourite_products = models.ManyToManyField(Product, blank=True)
    anonymous_user = models.BooleanField(default=False)
    use_saved_details = models.BooleanField(default=False)
    shipping_details_id = models.CharField(max_length=40)
    # Should have just used shipping details model
    email = models.EmailField(max_length=70,blank=True)
    name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    zip_code = models.CharField(max_length=40)
    localidade = models.CharField(max_length=40)
    cell_number = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username

def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)
