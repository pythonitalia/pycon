from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa
from .base import FRONTEND_URL, env

SECRET_KEY = env("SECRET_KEY")

if FRONTEND_URL == "http://testfrontend.it/":
    raise ImproperlyConfigured("Please configure FRONTEND_URL for production")
