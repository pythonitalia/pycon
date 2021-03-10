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
    """This service retrieves or creates a CheckoutSession and returns aggregating customer and subscription data

    @raises AlreadySubscribed
    """
    checkout_session = None

    subscription = await association_repository.get_subscription_by_user_id(
        user_data.user_id
    )

    if subscription:
        print(f"subscription : {subscription}")
        subscription_state = subscription.get_calculated_state()
        if subscription_state == SubscriptionState.PENDING:
            return subscription
        elif subscription_state == SubscriptionState.ACTIVE:
            raise AlreadySubscribed(expiration_date=subscription.expiration_date)
        elif subscription_state == SubscriptionState.EXPIRED:
            raise AlreadySubscribed(expiration_date=subscription.expiration_date)
        else:
            raise NotImplementedError(
                "This should not happen because subscription is in a not handled state"
            )

    if not checkout_session:
        customer = await association_repository.retrieve_customer_by_email(
            user_data.email
        )
        if customer:
            print(f"customer : {customer}")
            checkout_session = await association_repository.create_checkout_session(
                StripeCheckoutSessionInput(
                    customer_email=user_data.email, customer_id=customer.id
                )
            )
            print(f"checkout_session : {checkout_session}")
        else:
            checkout_session = await association_repository.create_checkout_session(
                StripeCheckoutSessionInput(
                    customer_email=user_data.email, customer_id=""
                )
            )
            print(f"checkout_session : {checkout_session}")

    if checkout_session:
        subscription = await association_repository.save_subscription(
            Subscription(
                user_id=user_data.user_id,
                stripe_session_id=checkout_session.id,
                stripe_customer_id=checkout_session.customer_id,
                creation_date=datetime.now(),
                state=SubscriptionState.PENDING,
                stripe_id=checkout_session.subscription_id or "",
                expiration_date=datetime.now(),
            )
        )
        print(f"subscription : {subscription}")
        await association_repository.commit()
        return subscription
    else:
        raise NotImplementedError(
            "This should not happen this service should return always a subscription"
        )
