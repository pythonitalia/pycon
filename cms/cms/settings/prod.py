from .base import *  # noqa
from .base import env

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = [
    "cms.python.it",
    "staging-cms.python.it",
    "pythonit-staging-cms.politesky-d9883aec.westeurope.azurecontainerapps.io",
    "pythonit-production-cms.blueisland-671ab1bc.westeurope.azurecontainerapps.io",
]
CSRF_TRUSTED_ORIGINS = [
    "https://cms.python.it",
    "https://staging-cms.python.it",
    "https://pythonit-staging-cms.politesky-d9883aec.westeurope.azurecontainerapps.io",
    "https://pythonit-production-cms.blueisland-671ab1bc.westeurope.azurecontainerapps.io",
]

DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"

AZURE_ACCOUNT_NAME = env("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = env("AZURE_ACCOUNT_KEY")
AZURE_CONTAINER = env("AZURE_CONTAINER")
AZURE_URL_EXPIRATION_SECS = 10 * 60
