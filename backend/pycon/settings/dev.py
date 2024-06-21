from .base import *  # noqa
from .base import env

SECRET_KEY = "do not use this in production"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CELERY_TASK_ALWAYS_EAGER = True

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")

HASHID_DEFAULT_SECRET_SALT = "do not use in prod"

CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]
