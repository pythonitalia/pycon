import stripe
from typing import Annotated, Union
from api.context import Info
import strawberry
from django.conf import settings
from api.permissions import IsAuthenticated
from association_membership.models import Membership, StripeCustomer


@strawberry.type
class AlreadySubscribed:
    message: str = "You are already subscribed"


@strawberry.type
class CheckoutSession:
    stripe_session_id: str


SubscribeUserResult = Annotated[
    Union[CheckoutSession, AlreadySubscribed],
    strawberry.union(name="SubscribeUserResult"),
]


@strawberry.mutation(permission_classes=[IsAuthenticated])
def subscribe_user_to_association(info: Info) -> SubscribeUserResult:
    user = info.context.request.user
    membership = Membership.objects.of_user(user).first()

    if not membership:
        membership = Membership.objects.create(user=user)
        stripe_customer = stripe.Customer.create(
            email=user.email, metadata={"user_id": user.id}
        )

        local_stripe_customer = StripeCustomer.objects.create(
            user_id=user.id, stripe_customer_id=stripe_customer.id
        )

    if membership.is_active:
        return AlreadySubscribed()

    if not local_stripe_customer:
        local_stripe_customer = StripeCustomer.objects.of_user(user).first()

    checkout_session = stripe.checkout.Session.create(
        success_url=f"{settings.ASSOCIATION_FRONTEND_URL}?membership-status=success#membership",
        cancel_url=f"{settings.ASSOCIATION_FRONTEND_URL}#membership",
        payment_method_types=["card"],
        mode="subscription",
        customer=local_stripe_customer.stripe_customer_id,
        # Note: if adding more line items, make sure webhook handlers
        # can handle it when fetching the period start/end dates
        line_items=[
            {
                "price": settings.STRIPE_SUBSCRIPTION_PRICE_ID,
                "quantity": 1,
            }
        ],
    )

    return CheckoutSession(stripe_session_id=checkout_session.id)
