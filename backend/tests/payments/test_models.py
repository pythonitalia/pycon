import pytest
from payments.models import Payment, StripePayment

from payments.models.error import PaymentError
from payments.models.provider_types import BANKTR_TYPE, STRIPE_TYPE

from payments.admin import refund as admin_refund

from stripe.error import StripeError
from stripe.stripe_object import StripeObject


def test_str():
    payment = Payment(
        amount=100,
        currency='EUR'
    )
    assert str(payment) == f'EUR 100 on {payment.created:%B %d, %Y %H:%m}'
    assert payment.provider == BANKTR_TYPE


@pytest.mark.django_db
def test_stripe_charge(mocker):
    mock_stripe_create = mocker.patch('payments.models.stripe_payment.stripe.Charge.create')
    mock_stripe_create.return_value = StripeObject(id="ch_1C6kfeJMsSxij9YCLoi3YHX3")
    stripe = StripePayment(
        amount=100,
        currency='eur',
        description='New association'
    )
    stripe.capture(token='right_token')
    assert stripe.provider == STRIPE_TYPE
    assert stripe.transaction_id == "ch_1C6kfeJMsSxij9YCLoi3YHX3"
    mock_stripe_create.assert_called_once_with(
        amount=10000, 
        currency='eur', 
        source='right_token',
        description='New association'
    )
    stripe.save()


@pytest.mark.django_db
def test_stripe_charge_errors(mocker):
    mock_stripe_create = mocker.patch('payments.models.stripe_payment.stripe.Charge.create')
    mock_stripe_create.side_effect = StripeError()
    stripe = StripePayment(
        amount=100,
        currency='eur'
    )
    with pytest.raises(PaymentError):
        stripe.capture(token='wrong_token')


@pytest.mark.django_db
def test_stripe_refund(mocker):
    mock_stripe_refund = mocker.patch('payments.models.stripe_payment.stripe.Refund.create')
    stripe = StripePayment(
        transaction_id="ch_1C6kfeJMsSxij9YCLoi3YHX3",
    )
    stripe.refund()
    mock_stripe_refund.assert_called_once_with(
        charge="ch_1C6kfeJMsSxij9YCLoi3YHX3"
    )


@pytest.mark.django_db
def test_stripe_refund_errors(mocker):
    mock_stripe_refund = mocker.patch('payments.models.stripe_payment.stripe.Refund.create')
    mock_stripe_refund.side_effect = StripeError()
    stripe = StripePayment(
        transaction_id="ch_1C6kfeJMsSxij9YCLoi3YHX3",
    )
    with pytest.raises(PaymentError):
        stripe.refund()


@pytest.mark.django_db
def test_admin_refund(mocker):
    payment_1 = Payment.objects.create(
        amount=100,
        currency='EUR'
    )
    payment_2 = Payment.objects.create(
        amount=100,
        currency='EUR'
    )
    payment_3 = StripePayment.objects.create(
        transaction_id="ch_1C6kfeJMsSxij9YCLoi3YHX3",
    )
    mock_stripe_refund = mocker.patch('payments.models.stripe_payment.stripe.Refund.create')
    admin_refund(None, None, Payment.objects.all())

    for payment in Payment.objects.all():
        payment.status = 'refund'

    mock_stripe_refund.assert_called_once_with(
        charge="ch_1C6kfeJMsSxij9YCLoi3YHX3"
    )