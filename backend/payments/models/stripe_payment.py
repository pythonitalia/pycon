
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

import stripe
from stripe.error import StripeError

from payments.models import Payment

from .provider_types import STRIPE_TYPE
from .error import PaymentError


stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePayment(Payment):

    transaction_id = models.CharField(
        _('transaction id'),
        max_length=255,
        blank=True,
        help_text=_('Id of the transaction, if applicable'),
    )

    def capture(self, **kwargs):
        try:
            charge = stripe.Charge.create(
                amount=int(self.amount * 100),
                currency=self.currency,
                source=kwargs['token'],
                description=self.description
            )
            self.transaction_id = charge.id
            self.status = 'completed'
            self.save()
        except StripeError as err:
            raise PaymentError(err)

    def refund(self):
        try:
            stripe.Refund.create(
                charge=self.transaction_id
            )
            super().refund()
        except StripeError as err:
            raise PaymentError(err)

    def _get_payment_type(self):
        return STRIPE_TYPE
