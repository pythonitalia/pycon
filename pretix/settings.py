from pretix.settings import *  # noqa

SECRET_KEY = "{{secret_key}}"

LOGGING["handlers"]["mail_admins"]["include_html"] = True  # noqa
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"  # noqa

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

# Allow all the languages
# see: pretix/settings.py#L425-L435
LANGUAGES = [(k, v) for k, v in ALL_LANGUAGES]  # noqa

USE_X_FORWARDED_HOST = True
SITE_URL = "https://tickets.pycon.it"

MAIL_FROM = SERVER_EMAIL = DEFAULT_FROM_EMAIL = "noreply@pycon.it"
MAIL_FROM_NOTIFICATIONS = MAIL_FROM
MAIL_FROM_ORGANIZERS = MAIL_FROM
EMAIL_HOST = "email-smtp.eu-central-1.amazonaws.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "{{mail_user}}"
EMAIL_HOST_PASSWORD = "{{mail_password}}"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_SUBJECT_PREFIX = "[PyCon Tickets] "

PRETIX_INSTANCE_NAME = "Python Italia"

# this is is needed for our hack that updates the order view
# without having to rewrite the whole template
CSP_ADDITIONAL_HEADER = "script-src 'self' 'unsafe-inline'"

# Config
PRETIX_REGISTRATION = False

VAT_ID_COUNTRIES = EU_COUNTRIES | {"CH", "NO", "GB"}

if "pretix_fattura_elettronica" in INSTALLED_APPS:  # noqa
    INSTALLED_APPS.remove("pretix_fattura_elettronica")  # noqa

    INSTALLED_APPS.insert(0, "pretix_fattura_elettronica")  # noqa
