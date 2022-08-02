from .base import *  # noqa

SECRET_KEY = "do not use this in production"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

PASTAPORTO_SECRET = env("PASTAPORTO_SECRET", default="pastaporto_xxxxxxxx")

USERS_SERVICE_URL = env("USERS_SERVICE")
ASSOCIATION_BACKEND_SERVICE = env("ASSOCIATION_BACKEND_SERVICE")
SERVICE_TO_SERVICE_SECRET = env("SERVICE_TO_SERVICE_SECRET")
