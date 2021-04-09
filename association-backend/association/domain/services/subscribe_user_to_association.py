import logging
from datetime import datetime

from association.domain.entities.stripe import StripeCheckoutSession
from association.domain.entities.subscriptions import (
    Subscription,
    SubscriptionState,
    UserData,
)
from association.domain.exceptions import (
    AlreadySubscribed,
    MultipleCustomerReturned,
    MultipleCustomerSubscriptionsReturned,
    StripeSubscriptionNotFound,
)
from association.domain.repositories import AssociationRepository

logger = logging.getLogger(__name__)


async def subscribe_user_to_association(
    user_data: UserData, association_repository: AssociationRepository
) -> StripeCheckoutSession:
    subscription = await association_repository.get_subscription_by_user_id(
        user_data.user_id
    )
    if subscription:
        if subscription.state == SubscriptionState.PENDING:
            try:
                subscription = await association_repository.sync_with_external_service(
                    subscription
                )
                await association_repository.save_subscription(subscription)
                await association_repository.commit()
            except MultipleCustomerSubscriptionsReturned as ex:
                raise ex
            except StripeSubscriptionNotFound:
                # subscription not modified
                pass

        if subscription.state in [
            SubscriptionState.ACTIVE,
            SubscriptionState.EXPIRED,
        ]:
            raise AlreadySubscribed()

    # Get customer_id
    if subscription and subscription.stripe_customer_id:
        customer_id = subscription.stripe_customer_id
    else:
        try:
            (
                customer,
                _created,
            ) = await association_repository.get_or_create_customer_by_email(
                user_data.email
            )
            customer_id = customer.id
        except MultipleCustomerReturned as ex:
            raise ex

    # CREATE OR UPDATE SUBSCRIPTION
    if not subscription:
        subscription = Subscription(
            user_id=user_data.user_id,
            stripe_customer_id=customer_id,
            state=SubscriptionState.PENDING,
            created_at=datetime.now(),
            modified_at=datetime.now(),
        )
        await association_repository.save_subscription(subscription)
        await association_repository.commit()
    else:
        # This is the case when a subscription pass to Stripe handling
        subscription.stripe_customer_id = customer_id
        subscription.state = SubscriptionState.PENDING
        subscription.modified_at = datetime.now()
        await association_repository.save_subscription(subscription)
        await association_repository.commit()

    # Create the checkout_session
    checkout_session: StripeCheckoutSession = (
        await association_repository.create_checkout_session(customer_id=customer_id)
    )
    return checkout_session
