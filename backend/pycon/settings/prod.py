import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa
from .base import DATABASES, MIDDLEWARE, env

SECRET_KEY = env("SECRET_KEY")
# CELERY_BROKER_URL = env("CELERY_BROKER_URL")
USE_SCHEDULER = False

# if FRONTEND_URL == "http://testfrontend.it/":
#     raise ImproperlyConfigured("Please configure FRONTEND_URL for production")

SENTRY_DSN = env("SENTRY_DSN", default="")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )

SLACK_INCOMING_WEBHOOK_URL = env("SLACK_INCOMING_WEBHOOK_URL")

DEFAULT_FILE_STORAGE = env(
    "DEFAULT_FILE_STORAGE", default="storages.backends.s3boto3.S3Boto3Storage"
)

AWS_STORAGE_BUCKET_NAME = env("AWS_MEDIA_BUCKET", default=None)
AWS_S3_REGION_NAME = env("AWS_REGION_NAME", default="eu-central-1")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default=None)

EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.locmem.EmailBackend"
)

FORCE_PYCON_HOST = env("FORCE_PYCON_HOST", bool, default=True)

if FORCE_PYCON_HOST:  # pragma: no cover
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    MIDDLEWARE += ["pycon.middleware.force_pycon_host"]

DEFAULT_FROM_EMAIL = "noreply@pycon.it"

SIMULATE_PRETIX_DB = False
DATABASES["pretix"] = {**DATABASES["default"], "NAME": "pretix"}
