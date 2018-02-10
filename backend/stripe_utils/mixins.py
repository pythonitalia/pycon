import stripe

from django.conf import settings


class StripeCustomerMixin:
    """
        Requires `customer_id`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(self, 'customer_id'):
            raise NotImplementedError()

    def get_orders(self):
        return stripe.Charge.list(customer=self.customer_id)
