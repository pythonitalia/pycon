from pretix.settings import *  # noqa
from pretix.settings import INSTALLED_APPS, ALL_LANGUAGES, LOGGING

LOGGING["handlers"]["mail_admins"]["include_html"] = True

# Allow all the languages
# see: pretix/settings.py#L425-L435
LANGUAGES = [(k, v) for k, v in ALL_LANGUAGES]

EMAIL_SUBJECT_PREFIX = "[PyCon Tickets] "

if "pretix_fattura_elettronica" in INSTALLED_APPS:
    INSTALLED_APPS.remove("pretix_fattura_elettronica")
    INSTALLED_APPS.insert(0, "pretix_fattura_elettronica")
