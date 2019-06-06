from django.utils.translation import ugettext_lazy as _


class PaymentFailedError(Exception):
    """
    This is a generic exception when we are not
    really able to give better instructions to the user.

    It should be possibile to override the message
    """
    def __init__(self, message=None):
        self.message = message or _("Unable to process your payment, please try again or contact your bank")

    def __str__(self):
        return self.message
