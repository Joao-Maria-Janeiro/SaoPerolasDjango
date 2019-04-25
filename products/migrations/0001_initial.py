# Generated by Django 2.1.2 on 2019-03-29 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('description', models.TextField()),
                ('price', models.CharField(max_length=5)),
                ('image', models.FileField(blank=True, upload_to='page_image')),
                ('pulseira', models.BooleanField()),
                ('brinco', models.BooleanField()),
                ('colar', models.BooleanField()),
            ],
        ),
    ]