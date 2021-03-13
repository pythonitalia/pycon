import logging

from pydantic import BaseModel

from association.domain.entities.stripe import StripeStatus
from association.domain.entities.subscriptions import SubscriptionState
from association.domain.exceptions import (
    InconsistentStateTransitionError,
    SubscriptionNotFound,
)
from association.domain.repositories.association_repository import AssociationRepository

logger = logging.getLogger(__name__)


class SubscriptionDetailInput(BaseModel):
    subscription_id: str
    status: str


async def handle_customer_subscription_updated(
    data: SubscriptionDetailInput, association_repository: AssociationRepository
):
    subscription = await association_repository.get_subscription_by_stripe_id(
        data.subscription_id
    )
    if subscription:
        # if subscription.is_for_life:
        #     subscription.state = SubscriptionState.ACTIVE
        if data.status == StripeStatus.ACTIVE:
            subscription.state = SubscriptionState.ACTIVE
        elif data.status == StripeStatus.INCOMPLETE:
            subscription.state = SubscriptionState.PENDING
        elif data.status == StripeStatus.INCOMPLETE_EXPIRED:
            if subscription.stripe_id:
                error_message = (
                    "This should not happen...INCOMPLETE_EXPIRED should happen only "
                    "when a subscription has never been created"
                )
                raise InconsistentStateTransitionError(error_message)
            subscription.state = SubscriptionState.NOT_CREATED
            # The session is expired, so the User cannot access that Session
            subscription.stripe_session_id = ""
        else:
            subscription.state = SubscriptionState.EXPIRED
        subscription = await association_repository.save_subscription(subscription)
        await association_repository.commit()
        return subscription
    else:
        msg = f"No Subscription found with subscription_id:{data.subscription_id}"
        logger.warning(msg)
        raise SubscriptionNotFound(msg)
