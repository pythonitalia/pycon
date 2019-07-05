from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from .stripe import Stripe


PROVIDER_STRIPE = 'stripe'
PROVIDER_BANK = 'bank'

PROVIDERS = Choices(
    (PROVIDER_STRIPE, _('Stripe')),
    (PROVIDER_BANK, _('Bank Transfer')),
)

PROVIDER_TO_IMPL = {
    PROVIDER_STRIPE: Stripe,
}


def get_provider(name):
    return PROVIDER_TO_IMPL.get(name, None)
