from .base import *  # noqa

SECRET_KEY = "this-key-should-only-be-used-for-tests"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
PASTAPORTO_SECRET = "pastaporto_test_xxx"

USERS_SERVICE_URL = "http://users-service"
ASSOCIATION_BACKEND_SERVICE = "http://association-service"
USERS_SERVICE = "http://fake-service"
SERVICE_TO_SERVICE_SECRET = "secret-to-secret"

MAILCHIMP_SECRET_KEY = "super-secret-key-for-tests"
MAILCHIMP_DC = "us5"
MAILCHIMP_LIST_ID = "12345678ab"

PRETIX_API = "http://pretix-api:9000/"
