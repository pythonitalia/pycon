from django.utils.translation import ugettext_lazy as _
from model_utils import Choices


STRIPE_TYPE = 'stripe'
BANKTR_TYPE = 'bank_transfer'


PROVIDER_TYPES = Choices(
    (BANKTR_TYPE, _('bank transfer')),
    (STRIPE_TYPE, _('stripe')),
)
