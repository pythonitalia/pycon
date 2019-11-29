from pretix.settings import *  # noqa

LOGGING["handlers"]["mail_admins"]["include_html"] = True  # noqa
STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
)  # noqa

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

USE_X_FORWARDED_HOST = True
SITE_URL = "https://d3ex7joy4im5c0.cloudfront.net"

MAIL_FROM = SERVER_EMAIL = DEFAULT_FROM_EMAIL = "noreply@pycon.it"
EMAIL_HOST = "email-smtp.us-east-1.amazonaws.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "{{mail_user}}"
EMAIL_HOST_PASSWORD = "{{mail_password}}"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_SUBJECT_PREFIX = "[PyCon Tickets] "
