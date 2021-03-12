import logging
from datetime import datetime

from association.domain.entities.stripe_entities import StripeCheckoutSessionInput
from association.domain.entities.subscription_entities import (
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
        print(f"subscription : {subscription}")
        subscription_state = subscription.state
        if subscription_state == SubscriptionState.PENDING:
            if subscription.stripe_session_id:
                return subscription
        elif subscription_state in [
            SubscriptionState.ACTIVE,
            SubscriptionState.EXPIRED,
        ]:
            raise AlreadySubscribed()
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
    print(f"customer_id : {customer_id}")

    checkout_session = await association_repository.create_checkout_session(
        StripeCheckoutSessionInput(
            customer_email=user_data.email, customer_id=customer_id
        )
    )
    print(f"checkout_session : {checkout_session}")

    subscription = await association_repository.save_subscription(
        Subscription(
            user_id=user_data.user_id,
            stripe_session_id=checkout_session.id,
            stripe_customer_id=checkout_session.customer_id,
            creation_date=datetime.now(),
            user_email=user_data.email,
            state=SubscriptionState.PENDING,
            stripe_id=checkout_session.subscription_id or "",
        )
    )
    print(f"subscription : {subscription}")
    await association_repository.commit()
    return subscription
