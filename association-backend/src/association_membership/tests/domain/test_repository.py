from datetime import datetime, timezone
from unittest.mock import patch

from ward import raises, test

from src.association.settings import STRIPE_SUBSCRIPTION_PRICE_ID
from src.association.tests.session import db
from src.association_membership.domain.entities import (
    InvoiceStatus,
    Subscription,
    SubscriptionInvoice,
    SubscriptionStatus,
)
from src.association_membership.domain.repository import AssociationMembershipRepository
from src.association_membership.tests.factories import SubscriptionFactory
from src.customers.tests.factories import CustomerFactory


@test("get subscription by stripe id")
async def _(db=db):
    subscription = await SubscriptionFactory(stripe_subscription_id="sub_test")

    repository = AssociationMembershipRepository()
    found_subscription = await repository.get_by_stripe_id("sub_test")

    assert found_subscription.id == subscription.id


@test("get subscription by not existent stripe id")
async def _(db=db):
    repository = AssociationMembershipRepository()
    found_subscription = await repository.get_by_stripe_id("sub_random_id")

    assert found_subscription is None


@test("create checkout session")
async def _(db=db):
    customer = await CustomerFactory(stripe_customer_id="cus_test")
    repository = AssociationMembershipRepository()

    with patch(
        "src.association_membership.domain.repository.stripe.checkout.Session.create"
    ) as mock_create:
        mock_create.return_value.id = "cs_xxxx"
        checkout_session_id = await repository.create_checkout_session(customer)

    assert mock_create.call_args.kwargs["mode"] == "subscription"
    assert mock_create.call_args.kwargs["line_items"] == [
        {
            "price": STRIPE_SUBSCRIPTION_PRICE_ID,
            "quantity": 1,
        }
    ]
    assert mock_create.call_args.kwargs["customer"] == "cus_test"
    assert checkout_session_id == "cs_xxxx"


@test("save subscription changes")
async def _(db=db):
    subscription = await SubscriptionFactory(status=SubscriptionStatus.ACTIVE)
    repository = AssociationMembershipRepository()

    subscription.status = SubscriptionStatus.CANCELED

    saved_subscription = await repository.save_subscription(subscription)
    assert saved_subscription.status == SubscriptionStatus.CANCELED

    # Check the change was saved in DB
    db_subscription = await Subscription.objects.get(id=subscription.id)
    assert db_subscription.status == SubscriptionStatus.CANCELED


@test("save subscription with new invoices")
async def _(db=db):
    subscription = await SubscriptionFactory()
    repository = AssociationMembershipRepository()

    now = datetime.now(timezone.utc)
    subscription.add_invoice(
        SubscriptionInvoice(
            status=InvoiceStatus.PAID,
            subscription=subscription,
            payment_date=now,
            period_start=now,
            period_end=now,
            stripe_invoice_id="inv_xxx",
            invoice_pdf="https://example.org/fake-invoice",
        )
    )

    await repository.save_subscription(subscription)

    # Check the change was saved in DB
    db_subscription = await Subscription.objects.select_related("invoices").get(
        id=subscription.id
    )

    assert len(db_subscription.invoices) == 1
    assert db_subscription.invoices[0].status == InvoiceStatus.PAID
    assert db_subscription.invoices[0].payment_date == now
    assert db_subscription.invoices[0].period_start == now
    assert db_subscription.invoices[0].period_end == now
    assert db_subscription.invoices[0].stripe_invoice_id == "inv_xxx"
    assert db_subscription.invoices[0].invoice_pdf == "https://example.org/fake-invoice"


@test("get or create subscription with existing subscription")
async def _(db=db):
    subscription = await SubscriptionFactory(stripe_subscription_id="sub_1")
    repository = AssociationMembershipRepository()

    found_subscription = await repository.get_or_create_subscription(
        customer=subscription.customer, stripe_subscription_id="sub_1"
    )

    assert found_subscription.id == subscription.id


@test(
    "get or create subscription fails if a subscription exists but for another customer"
)
async def _(db=db):
    customer = await CustomerFactory()
    await SubscriptionFactory(stripe_subscription_id="sub_1")
    repository = AssociationMembershipRepository()

    with raises(ValueError) as exc:
        await repository.get_or_create_subscription(
            customer=customer, stripe_subscription_id="sub_1"
        )

    assert str(exc.raised) == "Subscription found but assigned to another customer"


@test("get or create subscription creates a new subscription")
async def _(db=db):
    customer = await CustomerFactory()
    repository = AssociationMembershipRepository()

    found_subscription = await repository.get_or_create_subscription(
        customer=customer, stripe_subscription_id="sub_1"
    )

    assert found_subscription.id is not None
    assert found_subscription.stripe_subscription_id == "sub_1"
    assert found_subscription.customer.id == customer.id
