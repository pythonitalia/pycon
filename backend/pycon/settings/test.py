from .base import env
from .base import *  # noqa

IS_RUNNING_TESTS = True

SECRET_KEY = "this-key-should-only-be-used-for-tests"
HASHID_DEFAULT_SECRET_SALT = "only-for-tests"

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

MAILCHIMP_SECRET_KEY = "super-secret-key-for-tests"
MAILCHIMP_DC = "us5"
MAILCHIMP_LIST_ID = "12345678ab"

PRETIX_API = "https://pretix/api/"

STORAGES = {
    "default": {
        "BACKEND": "pycon.storages.CustomInMemoryStorage",
    },
    "private": {
        "BACKEND": "pycon.storages.CustomInMemoryStorage",
    },
    "localstorage": {
        "BACKEND": "pycon.storages.CustomInMemoryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
