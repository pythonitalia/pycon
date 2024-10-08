from .base import *  # noqa
from .base import env

SECRET_KEY = env("SECRET_KEY")

AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "public, max-age=31536000"}
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN", default=None)

EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.locmem.EmailBackend"
)

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# TODO: Make this setting dynamic
CSRF_TRUSTED_ORIGINS = [
    # Staging domain
    "https://pastaporto-admin.pycon.it",
    # Production domain
    "https://admin.pycon.it",
    "https://pycon.it",
]

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")

HASHID_DEFAULT_SECRET_SALT = env("HASHID_DEFAULT_SECRET_SALT")

SESSION_COOKIE_SECURE = True
