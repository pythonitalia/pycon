from payments.models import Payment
from payments.providers.stripe import StripeProvider


def test_str():
    x = Payment(
        total=100,
        currency='EUR'
    )

    assert str(x) == f'EUR 100 on {x.created:%B %d, %Y %H:%m}'


def test_get_provider_stripe():
    x = Payment(
        total=100,
        currency='EUR',
        provider=Payment.PROVIDERS.stripe
    )

    assert type(x.get_provider()) == StripeProvider


def test_get_provider_bank():
    x = Payment(
        total=100,
        currency='EUR',
        provider=Payment.PROVIDERS.bank_transfer
    )

    # TODO: do we need a provider for bank transfers
    assert x.get_provider() is None
