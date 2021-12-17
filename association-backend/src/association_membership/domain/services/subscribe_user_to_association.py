import logging

from pythonit_toolkit.pastaporto.entities import PastaportoUserInfo

from src.association_membership.domain.exceptions import AlreadySubscribed
from src.association_membership.domain.repository import AssociationMembershipRepository

logger = logging.getLogger(__name__)


async def subscribe_user_to_association(
    user: PastaportoUserInfo, *, association_repository: AssociationMembershipRepository
) -> str:
    subscription = await association_repository.get_user_subscription(user.id)

    if not subscription:
        subscription = await association_repository.create_subscription(user.id)
        await association_repository.create_stripe_customer(user)

    if subscription.is_active:
        raise AlreadySubscribed()

    checkout_session_id = await association_repository.create_checkout_session(
        subscription
    )
    return checkout_session_id
