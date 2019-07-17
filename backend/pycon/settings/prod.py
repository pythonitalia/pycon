from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa
from .base import FRONTEND_URL, env

SECRET_KEY = env("SECRET_KEY")
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
USE_SCHEDULER = True

if FRONTEND_URL == "http://testfrontend.it/":
    raise ImproperlyConfigured("Please configure FRONTEND_URL for production")
