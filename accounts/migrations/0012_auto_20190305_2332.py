# Generated by Django 2.1.7 on 2019-03-05 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20190305_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='shipping_details',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cart.ShippingDetails'),
        ),
    ]