from .base import *  # noqa

SECRET_KEY = "do not use this in production"
SLACK_INCOMING_WEBHOOK_URL = ""
USE_SCHEDULER = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
