from datetime import datetime, timedelta, timezone
from pythonit_toolkit.pastaporto.entities import PastaportoUserInfo
from ward import raises, test

from src.association_membership.domain.entities import Payment, PaymentStatus, StripeSubscriptionPayment, Subscription, SubscriptionStatus
from src.association_membership.domain.exceptions import AlreadySubscribed
from src.association_membership.domain.services.subscribe_user_to_association import (
    subscribe_user_to_association,
)
from src.association_membership.tests.fake_repository import (
    FakeAssociationMembershipRepository,
)


@test("subscribe user without existing customer profile")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it", is_staff=False)

    checkout_session_id = await subscribe_user_to_association(
        user,
        association_repository=FakeAssociationMembershipRepository(),
    )
    assert checkout_session_id == "cs_session_cus_test_1"


@test("subscribe user with active subscription fails")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it", is_staff=False)
    subscription = Subscription(
        user_id=user.id,
        status=SubscriptionStatus.ACTIVE
    )
    payment = Payment(
        total=1000,
        status=PaymentStatus.PAID,
        payment_date=datetime.now(timezone.utc),
        period_start=datetime.now(timezone.utc) + timedelta(days=0),
        period_end=datetime.now(timezone.utc) + timedelta(days=30),
    )
    StripeSubscriptionPayment(
        payment=payment,
        stripe_subscription_id='sub_abcabc',
        stripe_invoice_id='iv_abcabc',
        invoice_pdf='https://stripe.com/pdf/xxx'
    )

    with raises(AlreadySubscribed):
        await subscribe_user_to_association(
            user,
            association_repository=FakeAssociationMembershipRepository([subscription]),
        )


@test("subscribe user with canceled subscription works")
async def _():
    user = PastaportoUserInfo(id=1, email="test@email.it", is_staff=False)
    subscription = Subscription(
        user_id=user.id,
        status=SubscriptionStatus.CANCELED
    )
    payment = Payment(
        total=1000,
        status=PaymentStatus.PAID,
        payment_date=datetime.now(timezone.utc),
        period_start=datetime.now(timezone.utc) + timedelta(days=0),
        period_end=datetime.now(timezone.utc) + timedelta(days=30),
    )
    StripeSubscriptionPayment(
        payment=payment,
        stripe_subscription_id='sub_abcabc',
        stripe_invoice_id='iv_abcabc',
        invoice_pdf='https://stripe.com/pdf/xxx'
    )

    checkout_session_id = await subscribe_user_to_association(
        user,
        association_repository=FakeAssociationMembershipRepository([subscription]),
    )
    assert checkout_session_id == "cs_xxx"
