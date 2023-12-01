from .base import *  # noqa

SECRET_KEY = "do not use this in production"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CELERY_TASK_ALWAYS_EAGER = True
