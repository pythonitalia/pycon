from .base import *  # noqa
from .base import env

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = [
    "cms.python.it",
    "staging-cms.python.it",
    "pythonit-staging-cms.politesky-d9883aec.westeurope.azurecontainerapps.io",
]
CSRF_TRUSTED_ORIGINS = [
    "https://cms.python.it",
    "https://staging-cms.python.it",
    "https://pythonit-staging-cms.politesky-d9883aec.westeurope.azurecontainerapps.io",
]
