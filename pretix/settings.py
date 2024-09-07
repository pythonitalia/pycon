from pretix.settings import *  # noqa
from pretix.settings import INSTALLED_APPS, ALL_LANGUAGES, LOGGING

LOGGING["handlers"]["mail_admins"]["include_html"] = True  # noqa

# Allow all the languages
# see: pretix/settings.py#L425-L435
LANGUAGES = [(k, v) for k, v in ALL_LANGUAGES]  # noqa

EMAIL_SUBJECT_PREFIX = "[PyCon Tickets] "
PRETIX_INSTANCE_NAME = "Python Italia"

# this is is needed for our hack that updates the order view
# without having to rewrite the whole template
CSP_ADDITIONAL_HEADER = "script-src 'self' 'unsafe-inline'"

if "pretix_fattura_elettronica" in INSTALLED_APPS:  # noqa
    INSTALLED_APPS.remove("pretix_fattura_elettronica")  # noqa
    INSTALLED_APPS.insert(0, "pretix_fattura_elettronica")  # noqa
