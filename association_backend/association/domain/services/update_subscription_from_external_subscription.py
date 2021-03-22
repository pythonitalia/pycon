import logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from association.domain.entities.stripe import StripeStatus
from association.domain.entities.subscriptions import Subscription, SubscriptionState
from association.domain.exceptions import (
    InconsistentStateTransitionError,
    SubscriptionNotFound,
)
from association.domain.repositories.association_repository import AssociationRepository

logger = logging.getLogger(__name__)


class SubscriptionDetailInput(BaseModel):
    subscription_id: str
    status: str
    customer_id: Optional[str] = None
    canceled_at: Optional[datetime] = None


async def update_subscription_from_external_subscription(
    data: SubscriptionDetailInput,
    subscription: Optional[Subscription],
    association_repository: AssociationRepository,
):
    if not subscription:
        subscription = (
            await association_repository.get_subscription_by_stripe_subscription_id(
                data.subscription_id
            )
        )
    if subscription:
        if data.customer_id:
            subscription.customer_id = data.customer_id
        subscription.canceled_at = data.canceled_at
        # if subscription.is_for_life:
        #     subscription.state = SubscriptionState.ACTIVE
        if data.status == StripeStatus.ACTIVE:
            subscription.state = SubscriptionState.ACTIVE
        elif data.status == StripeStatus.INCOMPLETE:
            subscription.state = SubscriptionState.PENDING
        elif data.status == StripeStatus.INCOMPLETE_EXPIRED:
            if subscription.state in [
                SubscriptionState.ACTIVE,
                SubscriptionState.EXPIRED,
            ]:
                error_message = (
                    "This should not happen...the state INCOMPLETE_EXPIRED should be associated to"
                    "a subscription with status PENDING"
                )
                raise InconsistentStateTransitionError(error_message)
            if len(subscription.subscription_payments):
                error_message = (
                    "This should not happen...the state INCOMPLETE_EXPIRED should be associated to"
                    "a subscription without associated Payments"
                )
                raise InconsistentStateTransitionError(error_message)
            subscription.state = SubscriptionState.FIRST_PAYMENT_EXPIRED
            # the User cannot access the old Session or Subscription
            subscription.stripe_session_id = ""
            subscription.stripe_subscription_id = ""
        elif data.status in [
            StripeStatus.CANCELED,
            StripeStatus.UNPAID,
        ]:
            subscription.state = SubscriptionState.CANCELED
            # the User cannot access the old Session or Subscription
            subscription.stripe_session_id = ""
            subscription.stripe_subscription_id = ""
        else:
            # This is not a terminal state because User can change his payment settings going to customer portal
            subscription.state = SubscriptionState.EXPIRED
        subscription = await association_repository.save_subscription(subscription)
        await association_repository.commit()
        return subscription
    else:
        msg = f"No Subscription found with subscription_id:{data.subscription_id}"
        logger.warning(msg)
        raise SubscriptionNotFound(msg)
