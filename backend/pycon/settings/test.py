from .base import *  # noqa

SECRET_KEY = "this-key-should-only-be-used-for-tests"
SLACK_INCOMING_WEBHOOK_URL = ""
USE_SCHEDULER = False
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
