import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa
from .base import env

SECRET_KEY = env("SECRET_KEY")
# CELERY_BROKER_URL = env("CELERY_BROKER_URL")
USE_SCHEDULER = False

# if FRONTEND_URL == "http://testfrontend.it/":
#     raise ImproperlyConfigured("Please configure FRONTEND_URL for production")

SENTRY_DSN = env("SENTRY_DSN", default="")

if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])

SLACK_INCOMING_WEBHOOK_URL = env("SLACK_INCOMING_WEBHOOK_URL")
