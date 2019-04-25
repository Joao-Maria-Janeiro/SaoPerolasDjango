from django import forms
from .models import ShippingDetails

class CreateShipphingDetails(forms.ModelForm):

    class Meta:
        model = ShippingDetails
        fields = ('full_name', 'adress', 'city', 'localidade', 'zip', 'country', 'phone_number', 'email')
