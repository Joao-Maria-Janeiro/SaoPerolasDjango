from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    price = models.CharField(max_length=5)
    image = models.FileField(upload_to='page_image', blank=True)
    pulseira = models.BooleanField()
    brinco = models.BooleanField()
    colar = models.BooleanField()

    def __str__(self):
        return 'Name: {}, ID: {}'.format(self.name, self.id)

class BackGroundImage(models.Model):
    image = models.FileField(upload_to='background', blank=True)
