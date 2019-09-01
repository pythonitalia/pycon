from .base import *  # noqa
from .base import env

SECRET_KEY = env("SECRET_KEY")
# CELERY_BROKER_URL = env("CELERY_BROKER_URL")
USE_SCHEDULER = False

# if FRONTEND_URL == "http://testfrontend.it/":
#     raise ImproperlyConfigured("Please configure FRONTEND_URL for production")


DEFAULT_FILE_STORAGE = env("DEFAULT_FILE_STORAGE", default="storages.backends.s3boto3.S3Boto3Storage")
AWS_STORAGE_BUCKET_NAME = env("AWS_MEDIA_BUCKET")
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
