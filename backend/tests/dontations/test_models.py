import pytest
from donations.models import Donation
from users.models import User
from stripe.stripe_object import StripeObject
from stripe.error import StripeError


@pytest.mark.django_db
def test_create_donation_with_stripe(mocker):

    mock_stripe_create = mocker.patch('payments.models.stripe_payment.stripe.Charge.create')
    mock_stripe_create.return_value = StripeObject(id="ch_1C6kfeJMsSxij9YCLoi3YHX3")

    user = User.objects.create_user('lennon@thebeatles.com', 'johnpassword')
    donation = Donation.create_donation_with_stripe('visa_token', user, 10, True)

    donation = Donation.objects.all()[0]

    donation.payment.amount = 10
    donation.payment.transaction_id = "ch_1C6kfeJMsSxij9YCLoi3YHX3"


@pytest.mark.django_db
def test_create_donation_with_stripe_error(mocker):

    mock_stripe_create = mocker.patch('payments.models.stripe_payment.stripe.Charge.create')
    mock_stripe_create.side_effect = StripeError()

    user = User.objects.create_user('lennon@thebeatles.com', 'johnpassword')
    donation = Donation.create_donation_with_stripe('visa_token', user, 10, True)

    assert len(Donation.objects.all()) == 0