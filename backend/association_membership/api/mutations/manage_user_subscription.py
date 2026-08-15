import stripe
from typing import Annotated, Union
from api.context import Info
import strawberry

from api.permissions import IsAuthenticated
from association_membership.models import StripeCustomer, Membership


@strawberry.type
class NoSubscription:
    message: str = "No subscription to manage"


@strawberry.type
class NotSubscribedViaStripe:
    message: str = "Not subscribed via Stripe"


@strawberry.type
class CustomerPortalResponse:
    billing_portal_url: str


CustomerPortalResult = Annotated[
    Union[CustomerPortalResponse, NoSubscription, NotSubscribedViaStripe],
    strawberry.union(name="CustomerPortalResult"),
]


@strawberry.mutation(permission_classes=[IsAuthenticated])
def manage_user_subscription(info: Info) -> CustomerPortalResult:
    membership = Membership.objects.active().of_user(info.context.request.user).first()

    if not membership:
        return NoSubscription()

    stripe_customer = StripeCustomer.objects.of_user(info.context.request.user).first()

    if not stripe_customer:
        return NotSubscribedViaStripe()

    session = stripe.billing_portal.Session.create(
        customer=stripe_customer.stripe_customer_id
    )
    billing_portal_url = session.url
    return CustomerPortalResponse(billing_portal_url=billing_portal_url)
