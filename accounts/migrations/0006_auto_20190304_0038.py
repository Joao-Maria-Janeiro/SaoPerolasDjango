# Generated by Django 2.1.7 on 2019-03-04 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190127_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='anonymous_user',
            field=models.BooleanField(default=False),
        ),
    ]
