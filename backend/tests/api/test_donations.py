import pytest

from donations.api.mutations import DonateWithStripe

from unittest.mock import MagicMock
from users.models import User


@pytest.mark.django_db
def test_donations():
    donate_with_stripe = DonateWithStripe()
    donate_with_stripe_input = MagicMock(
        token='token_valid',
        amount=10.0,
        is_public=True
    )
    user = User.objects.create_user('lennon@thebeatles.com', 'johnpassword')
    info = MagicMock()
    info.context.user = user
    donate_with_stripe.mutate(info, donate_with_stripe_input)
