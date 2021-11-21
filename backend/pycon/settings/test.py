from .base import *  # noqa

SECRET_KEY = "this-key-should-only-be-used-for-tests"
SLACK_INCOMING_WEBHOOK_URL = ""
USE_SCHEDULER = False
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
PASTAPORTO_SECRET = "pastaporto_test_xxx"

USERS_SERVICE = "http://fake-service"
SERVICE_TO_SERVICE_SECRET = "secret-to-secret"

MAILCHIMP_SECRET_KEY = "super-secret-key-for-tests"
MAILCHIMP_DC = "us5"
MAILCHIMP_LIST_ID = "12345678ab"
