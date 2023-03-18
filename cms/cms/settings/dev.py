from .base import *  # noqa

SECRET_KEY = "django-insecure-ss+@vr3zfthhbi%i7epq=6ul1pu-)(wgi@(am^3u-!g#eq@=8l"
ALLOWED_HOSTS = ["*"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *  # noqa
except ImportError:
    pass
