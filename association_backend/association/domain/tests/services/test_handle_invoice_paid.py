import datetime

from ward import raises, test

from association.domain import services
from association.domain.exceptions import SubscriptionNotFound
from association.domain.services import InvoicePaidInput
from association.domain.tests.repositories.fake_repository import (
    FakeAssociationRepository,
)
from association.tests.factories import SubscriptionFactory


@test("Subscription payed")
async def _():
    sut_subscription = SubscriptionFactory(
        stripe_id="sub_test_1234",
    )
    assert sut_subscription.stripe_id == "sub_test_1234"

    repository = FakeAssociationRepository(
        subscriptions=[sut_subscription], customers=[]
    )

    subscription = await services.handle_invoice_paid(
        invoice_input=InvoicePaidInput(
            subscription_id=sut_subscription.stripe_id,
            paid_at=datetime.datetime(2020, 4, 1, 0, 0).astimezone().timestamp(),
            invoice_id="in_test_12345",
            invoice_pdf="https://stripe.com/pdf/invoice_test_1234",
        ),
        association_repository=repository,
    )
    payment = subscription.subscription_payments[0]
    assert payment.subscription == subscription
    assert payment.payment_date == datetime.datetime(2020, 4, 1, 0, 0).astimezone()
    assert payment.invoice_id == "in_test_12345"
    assert payment.invoice_pdf == "https://stripe.com/pdf/invoice_test_1234"


@test("SubscriptionNotFound raised")
async def _():
    repository = FakeAssociationRepository(subscriptions=[], customers=[])

    with raises(SubscriptionNotFound):
        await services.handle_invoice_paid(
            invoice_input=InvoicePaidInput(
                subscription_id=SubscriptionFactory().stripe_id,
                paid_at=datetime.datetime(2020, 4, 1, 0, 0).timestamp(),
                invoice_id="in_test_12345",
                invoice_pdf="https://stripe.com/pdf/invoice_test_1234",
            ),
            association_repository=repository,
        )
