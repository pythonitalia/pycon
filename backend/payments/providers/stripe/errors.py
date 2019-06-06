from django.utils.translation import ugettext_lazy as _


class Stripe3DVerificationError(Exception):
    message = _("Stripe payment failed because we need to verify it's really you")

    def __init__(self, client_secret):
        self.client_secret = client_secret

    def __str__(self):
        return self.message
