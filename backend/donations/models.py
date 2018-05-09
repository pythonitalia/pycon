from django.conf import settings
from django.db import models, transaction

from model_utils.models import TimeStampedModel

from payments.models import StripePayment
from payments.models.error import PaymentError

class Donation(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey('payments.Payment', on_delete=models.PROTECT)
    public = models.BooleanField(default=True)

    @classmethod
    def create_donation_with_stripe(self, token, user, amount, is_public):
        try:
            with transaction.atomic():
                donation = Donation(user=user, public=is_public)
                payment = StripePayment(amount=amount, currency='eur')
                payment.capture(token=token)
                donation.payment = payment
                donation.save()
                return donation
        except PaymentError:
            pass
