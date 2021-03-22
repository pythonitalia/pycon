import logging
from datetime import datetime

from association.domain import services
from association.domain.entities.stripe import StripeCheckoutSessionInput
from association.domain.entities.subscriptions import (
    Subscription,
    SubscriptionState,
    UserData,
)
from association.domain.exceptions import AlreadySubscribed, MultipleCustomerReturned
from association.domain.repositories import AssociationRepository
from association.domain.services.update_subscription_from_external_subscription import (
    SubscriptionDetailInput,
)

logger = logging.getLogger(__name__)


async def subscribe_user_to_association(
    user_data: UserData, association_repository: AssociationRepository
) -> Subscription:
    subscription = await association_repository.get_subscription_by_user_id(
        user_data.user_id
    )
    if subscription:
        logger.debug(f"{subscription = }")
        if (
            subscription.state == SubscriptionState.PENDING
            and not subscription.has_external_subscription()
        ):
            # We have to be sure that the first checkout Session has been completed or is FIRST_PAYMENT_EXPIRED.
            # We don't have the related subscription in case the first payment is not accomplished.
            # The session is opened and should be provisioned for the first 23 hours;
            # after this period we have to invalidate the old checkout session, but let us get the info from external service
            # See https://stripe.com/docs/upgrades#2019-03-14 for more info
            external_subscription = await association_repository.retrieve_external_subscription_by_session_id(
                subscription.stripe_session_id
            )
            if external_subscription:
                subscription = (
                    await services.update_subscription_from_external_subscription(
                        data=SubscriptionDetailInput(
                            subscription_id=external_subscription.id,
                            status=external_subscription.status,
                            customer_id=external_subscription.customer_id,
                            canceled_at=external_subscription.canceled_at,
                        ),
                        subscription=subscription,
                        association_repository=association_repository,
                    )
                )
                await association_repository.save_subscription(subscription)
                await association_repository.commit()
                logger.debug(f"{subscription = }")
        if subscription.state == SubscriptionState.PENDING:
            return subscription
        elif subscription.state in [
            SubscriptionState.ACTIVE,
            SubscriptionState.EXPIRED,
        ]:
            raise AlreadySubscribed()
        elif subscription.state in [
            SubscriptionState.FIRST_PAYMENT_EXPIRED,
            SubscriptionState.CANCELED,
        ]:
            # subscription not created or canceled has to be updated passing from a new Checkout Session
            # This will be deleted before new Subscription creation
            pass
        else:
            raise NotImplementedError(
                "This should not happen because subscription is in a not handled state"
            )

    # Get customer_id
    if subscription and subscription.stripe_customer_id:
        customer_id = subscription.stripe_customer_id
    else:
        try:
            customer = await association_repository.retrieve_customer_by_email(
                user_data.email
            )
            customer_id = customer and customer.id or ""
        except MultipleCustomerReturned as ex:
            raise ex
    logger.debug(f"{customer_id = }")

    # Create the checkout_session
    checkout_session = await association_repository.create_checkout_session(
        StripeCheckoutSessionInput(
            customer_email=user_data.email, customer_id=customer_id
        )
    )
    logger.debug(f"{checkout_session = }")

    # Save the subscription from the checkout session
    if subscription:
        # subscription = await association_repository.update_subscription_from_checkout_session(
        #     subscription, checkout_session
        # )
        subscription.state = SubscriptionState.PENDING
        subscription.stripe_session_id = checkout_session.id
        subscription.stripe_customer_id = checkout_session.customer_id
        subscription.stripe_subscription_id = checkout_session.subscription_id or ""
    else:
        # subscription = await association_repository.create_subscription_from_checkout_session(
        #     checkout_session
        # )
        subscription = Subscription(
            user_id=user_data.user_id,
            creation_date=datetime.now(),
            state=SubscriptionState.PENDING,
            stripe_session_id=checkout_session.id,
            stripe_customer_id=checkout_session.customer_id,
            stripe_subscription_id=checkout_session.subscription_id or "",
        )
    subscription = await association_repository.save_subscription(subscription)
    logger.debug(f"{subscription = }")
    await association_repository.commit()
    return subscription
