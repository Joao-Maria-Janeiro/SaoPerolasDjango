# Generated by Django 2.1.2 on 2019-03-05 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '__first__'),
        ('accounts', '0017_remove_userprofile_shipping_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='shipping_details',
            field=models.ManyToManyField(blank=True, to='cart.ShippingDetails'),
        ),
    ]
