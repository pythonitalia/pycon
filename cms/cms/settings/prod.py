from .base import *  # noqa
from .base import env

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = [
    "cms.python.it",
    "pastaporto-cms.python.it",
    "pythonit-staging-cms.politesky-d9883aec.westeurope.azurecontainerapps.io",
]
