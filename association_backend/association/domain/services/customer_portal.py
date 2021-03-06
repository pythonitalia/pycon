import logging

from association.domain.entities.subscription_entities import Subscription, UserData
from association.domain.exceptions import CustomerNotAvailable
from association.domain.repositories import AssociationRepository

logger = logging.getLogger(__name__)


async def customer_portal(
    user_data: UserData, association_repository: AssociationRepository
) -> Subscription:
    """This service creates a CustomerPortalSession and returns his url

    """
    subscription = await association_repository.get_subscription_by_user_id(
        user_data.user_id
    )
    if subscription.stripe_customer_id:
        billing_portal_url = await association_repository.retrieve_customer_portal_session_url(
            subscription.stripe_customer_id
        )
        return billing_portal_url
    else:
        raise CustomerNotAvailable()
