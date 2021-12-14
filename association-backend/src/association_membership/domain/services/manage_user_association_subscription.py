import logging

from pythonit_toolkit.pastaporto.entities import PastaportoUserInfo

from src.association_membership.domain.entities import Subscription
from src.association_membership.domain.exceptions import (
    CustomerNotAvailable,
    NoSubscriptionAvailable,
    NotSubscribedViaStripe,
)
from src.association_membership.domain.repository import AssociationMembershipRepository

logger = logging.getLogger(__name__)


async def manage_user_association_subscription(
    user: PastaportoUserInfo,
    *,
    association_repository: AssociationMembershipRepository,
) -> Subscription:
    """This service creates a CustomerPortalSession and returns its url"""
    subscription = await association_repository.get_user_subscription(user.id)

    if not subscription:
        raise CustomerNotAvailable()

    if not subscription.is_active:
        raise NoSubscriptionAvailable()

    stripe_customer = await association_repository.get_stripe_customer_from_user_id(
        user.id
    )

    if not stripe_customer:
        raise NotSubscribedViaStripe()

    billing_portal_url = await association_repository.create_stripe_portal_session_url(
        stripe_customer
    )
    return billing_portal_url
