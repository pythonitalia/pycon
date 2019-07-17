from secrets import token_urlsafe

from .base import *  # noqa
from .base import env

SECRET_KEY = token_urlsafe()
DEBUG = False

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
SLACK_INCOMING_WEBHOOK_URL = env("SLACK_INCOMING_WEBHOOK_URL")
