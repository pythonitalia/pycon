from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa
from .base import STRIPE_SECRET_KEY

SECRET_KEY = "this-key-should-only-be-used-for-tests"
SLACK_INCOMING_WEBHOOK_URL = ""
USE_SCHEDULER = False

if not STRIPE_SECRET_KEY.startswith("sk_test_"):
    raise ImproperlyConfigured("Stripe key does not seem a test key")
