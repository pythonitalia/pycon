from .base import *  # noqa
from .base import DATABASES, env, AWS_STORAGE_BUCKET_NAME

SECRET_KEY = env("SECRET_KEY")

AWS_S3_FILE_OVERWRITE = False
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "public, max-age=31536000"}
AWS_DEFAULT_ACL = "public-read"
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN", default=None)

EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.locmem.EmailBackend"
)

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DEFAULT_FROM_EMAIL = "noreply@pycon.it"

SIMULATE_PRETIX_DB = False
DATABASES["pretix"] = {**DATABASES["default"], "NAME": "pretix"}

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

AWS_CLOUDFRONT_KEY_FILE = env("AWS_CLOUDFRONT_KEY_FILE", default=None)
if AWS_CLOUDFRONT_KEY_FILE:
    import boto3
    from io import BytesIO

    buffer = BytesIO()

    s3 = boto3.client("s3")
    s3.download_fileobj(AWS_STORAGE_BUCKET_NAME, AWS_CLOUDFRONT_KEY_FILE, buffer)

    AWS_CLOUDFRONT_KEY = buffer.getvalue().decode("ascii")

AWS_CLOUDFRONT_KEY_ID = env("AWS_CLOUDFRONT_KEY_ID", default=None)
