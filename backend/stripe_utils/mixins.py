from django.db import models
from django.utils.translation import ugettext_lazy as _


class StripeCustomerMixin:
    """
        Requires `customer_id`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not hasattr(self, 'customer_id'):
            raise NotImplementedError()
