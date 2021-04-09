import logging

from association.domain.entities.stripe import StripeSubscription
from association.domain.exceptions import SubscriptionNotFound
from association.domain.repositories.association_repository import AssociationRepository

logger = logging.getLogger(__name__)


async def update_subscription_from_external_subscription(
    stripe_subscription: StripeSubscription,
    association_repository: AssociationRepository,
):
    subscription = (
        await association_repository.get_subscription_by_stripe_subscription_id(
            stripe_subscription.id
        )
    )
    if not subscription:
        subscription = (
            await association_repository.get_subscription_by_stripe_customer_id(
                stripe_subscription.customer_id
            )
        )

    if subscription:
        subscription = subscription.sync_with_stripe_subscription(
            stripe_subscription=stripe_subscription
        )

        subscription = await association_repository.save_subscription(subscription)
        await association_repository.commit()
        return subscription
    else:
        msg = f"No Subscription found with subscription_id:{stripe_subscription.id} and customer_id: {stripe_subscription.customer_id}"
        logger.warning(msg)
        raise SubscriptionNotFound(msg)
