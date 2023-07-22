from .base import *  # noqa

SECRET_KEY = "this-key-should-only-be-used-for-tests"

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

AZURE_STORAGE_ACCOUNT_NAME = "pytest-fakestorageaccount"
AZURE_STORAGE_ACCOUNT_KEY = "fake-key"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "conferencevideos": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

IMAGEKIT_DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
