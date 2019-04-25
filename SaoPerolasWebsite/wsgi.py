"""
WSGI config for saoperolasWebsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SaoPerolasWebsite.settings')

application = get_wsgi_application()

# Use whitenoise package to serve static files on Heroku
# from whitenoise import WhiteNoise
# from django.conf import settings
# from whitenoise.django import DjangoWhiteNoise
# # application = DjangoWhiteNoise(application)
#
# application = WhiteNoise(
#     DjangoWhiteNoise(get_wsgi_application()),
#     root=settings.MEDIA_ROOT,
#     prefix='/media/',
# )

from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling

application = Cling(MediaCling(get_wsgi_application()))
