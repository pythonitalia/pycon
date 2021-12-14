from datetime import datetime, timedelta, timezone

from pythonit_toolkit.pastaporto.entities import PastaportoUserInfo
from ward import raises, test

from src.association_membership.domain.entities import (
    Payment,
    PaymentStatus,
    PretixPayment,
    StripeCustomer,
    StripeSubscriptionPayment,
    Subscription,
    SubscriptionStatus,
)
from src.association_membership.domain.exceptions import (
    CustomerNotAvailable,
    NoSubscriptionAvailable,
    NotSubscribedViaStripe,
)
from src.association_membership.domain.services.manage_user_association_subscription import (
    manage_user_association_subscription,
)
from src.association_membership.tests.fake_repository import (
    FakeAssociationMembershipRepository,
)


@test("manage subscription user")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it", is_staff=False)
    subscription = Subscription(id=1, user_id=user.id, status=SubscriptionStatus.ACTIVE)
    payment = Payment(
        id=1,
        idempotency_key="iv_abcabc",
        subscription=subscription,
        total=1000,
        status=PaymentStatus.PAID,
        payment_date=datetime.now(timezone.utc),
        period_start=datetime.now(timezone.utc) + timedelta(days=0),
        period_end=datetime.now(timezone.utc) + timedelta(days=30),
    )
    StripeSubscriptionPayment(
        id=1,
        payment=payment,
        stripe_subscription_id="sub_abcabc",
        stripe_invoice_id="iv_abcabc",
        invoice_pdf="https://stripe.com/pdf/xxx",
    )
    stripe_customer = StripeCustomer(
        id=1, user_id=user.id, stripe_customer_id="cus_123"
    )

    fake_repository = FakeAssociationMembershipRepository(
        [subscription], [stripe_customer]
    )

    billing_portal_url = await manage_user_association_subscription(
        user, association_repository=fake_repository
    )

    assert billing_portal_url == "https://fake.stripe/customerportal/cus_hello"


@test("with no active subscription fails")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it", is_staff=False)
    subscription = Subscription(
        id=1, user_id=user.id, status=SubscriptionStatus.CANCELED
    )
    payment = Payment(
        id=1,
        total=1000,
        idempotency_key="iv_abcabc",
        subscription=subscription,
        status=PaymentStatus.PAID,
        payment_date=datetime.now(timezone.utc),
        period_start=datetime.now(timezone.utc) + timedelta(days=0),
        period_end=datetime.now(timezone.utc) + timedelta(days=30),
    )
    StripeSubscriptionPayment(
        id=1,
        payment=payment,
        stripe_subscription_id="sub_abcabc",
        stripe_invoice_id="iv_abcabc",
        invoice_pdf="https://stripe.com/pdf/xxx",
    )
    stripe_customer = StripeCustomer(
        id=1, user_id=user.id, stripe_customer_id="cus_123"
    )

    fake_repository = FakeAssociationMembershipRepository(
        [subscription], [stripe_customer]
    )

    with raises(NoSubscriptionAvailable):
        await manage_user_association_subscription(
            user, association_repository=fake_repository
        )


@test("with no subscription fails")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it", is_staff=False)
    fake_repository = FakeAssociationMembershipRepository([], [])

    with raises(CustomerNotAvailable):
        await manage_user_association_subscription(
            user, association_repository=fake_repository
        )


@test("when subscribed via other means than stripe fails to manage")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it", is_staff=False)
    subscription = Subscription(id=1, user_id=user.id, status=SubscriptionStatus.ACTIVE)
    payment = Payment(
        id=1,
        total=1000,
        idempotency_key="iv_abcabc",
        subscription=subscription,
        status=PaymentStatus.PAID,
        payment_date=datetime.now(timezone.utc),
        period_start=datetime.now(timezone.utc) + timedelta(days=0),
        period_end=datetime.now(timezone.utc) + timedelta(days=30),
    )
    PretixPayment(
        id=1,
        payment=payment,
        order_code="ABC",
    )

    fake_repository = FakeAssociationMembershipRepository([subscription], [])

    with raises(NotSubscribedViaStripe):
        await manage_user_association_subscription(
            user, association_repository=fake_repository
        )
