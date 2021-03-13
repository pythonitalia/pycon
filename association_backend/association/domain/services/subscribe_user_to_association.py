import logging
from datetime import datetime

from association.domain.entities.stripe import StripeCheckoutSessionInput
from association.domain.entities.subscriptions import (
    Subscription,
    SubscriptionState,
    UserData,
)
from association.domain.exceptions import AlreadySubscribed
from association.domain.repositories import AssociationRepository

logger = logging.getLogger(__name__)


async def subscribe_user_to_association(
    user_data: UserData, association_repository: AssociationRepository
) -> Subscription:
    subscription = await association_repository.get_subscription_by_user_id(
        user_data.user_id
    )
    if subscription:
        logger.debug(f"subscription : {subscription}")
        subscription_state = subscription.state
        if subscription_state == SubscriptionState.PENDING:
            return subscription
        elif subscription_state in [
            SubscriptionState.ACTIVE,
            SubscriptionState.EXPIRED,
        ]:
            raise AlreadySubscribed()
        elif subscription_state == SubscriptionState.NOT_CREATED:
            # subscription not created has to be recreated passing from a new Checkout Session
            pass
        else:
            raise NotImplementedError(
                "This should not happen because subscription is in a not handled state"
            )

    if subscription and subscription.stripe_customer_id:
        customer_id = subscription.stripe_customer_id
    else:
        customer = await association_repository.retrieve_customer_by_email(
            user_data.email
        )
        customer_id = customer and customer.id or ""
    logger.debug(f"customer_id : {customer_id}")

    checkout_session = await association_repository.create_checkout_session(
        StripeCheckoutSessionInput(
            customer_email=user_data.email, customer_id=customer_id
        )
    )
    logger.debug(f"checkout_session : {checkout_session}")

    subscription = await association_repository.save_subscription(
        # TODO Test this is a update_or_create
        Subscription(
            user_id=user_data.user_id,
            stripe_session_id=checkout_session.id,
            stripe_customer_id=checkout_session.customer_id,
            creation_date=datetime.now(),
            state=SubscriptionState.PENDING,
            stripe_id=checkout_session.subscription_id or "",
        )
    )
    logger.debug(f"subscription : {subscription}")

    await association_repository.commit()
    return subscription
