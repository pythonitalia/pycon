import os

from pretix.settings import *

os.environ["PRETIX_CONFIG_FILE"] = "/pretix/pretix.cfg"


SECRET_KEY = 123

LOGGING["handlers"]["mail_admins"]["include_html"] = True
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "{{database_name}}",
        "USER": "{{database_username}}",
        "PASSWORD": "{{database_password}}",
        "HOST": "{{database_host}}",
        "PORT": "5432",
    }
}

MAIL_FROM = SERVER_EMAIL = DEFAULT_FROM_EMAIL = "noreply@pycon.it"
EMAIL_HOST = "email-smtp.eu-west-1.amazonaws.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "{{mail_user}}"
EMAIL_HOST_PASSWORD = "{{mail_password}}"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = "[PyCon Tickets] "
