from .base import *  # noqa

from secrets import token_urlsafe

SECRET_KEY = token_urlsafe()

CELERY_BROKER_URL = env('CELERY_BROKER_URL')
