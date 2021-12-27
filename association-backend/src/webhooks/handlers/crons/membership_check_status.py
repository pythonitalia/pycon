import logging
from datetime import datetime, timezone
from typing import Any

from src.association_membership.domain.entities import (
    PaymentStatus,
    Subscription,
    SubscriptionStatus,
)
from src.association_membership.domain.repository import AssociationMembershipRepository

logger = logging.getLogger(__file__)


async def membership_check_status(payload: Any):
    await update_expired_subscriptions()
    await update_now_active_subscriptions()


async def update_now_active_subscriptions():
    repository = AssociationMembershipRepository()

    now = datetime.now(timezone.utc)
    # Ideally in the future we should use the psql NOW() function
    qs = Subscription.objects.filter(
        status=SubscriptionStatus.CANCELED,
        payments__status=PaymentStatus.PAID,
        payments__period_start__lte=now,
        payments__period_end__gte=now,
    )
    subscriptions_to_enable = await qs.all()
    subscriptions_to_enable_count = await qs.count()

    logger.info(
        "Found subscriptions_to_enable_count=%s subscriptions to activate",
        subscriptions_to_enable_count,
    )

    for subscription in subscriptions_to_enable:
        subscription.mark_as_active()
        await repository.save_subscription(subscription)


async def update_expired_subscriptions():
    repository = AssociationMembershipRepository()

    now = datetime.now(timezone.utc)
    # Ideally in the future we should use the psql NOW() function
    qs = Subscription.objects.filter(status=SubscriptionStatus.ACTIVE,).exclude(
        payments__status=PaymentStatus.PAID,
        payments__period_start__lte=now,
        payments__period_end__gte=now,
    )
    subscriptions_to_cancel = await qs.all()
    subscriptions_to_cancel_count = await qs.count()

    logger.info(
        "Found subscriptions_to_cancel_count=%s subscriptions to cancel",
        subscriptions_to_cancel_count,
    )

    for subscription in subscriptions_to_cancel:
        subscription.mark_as_canceled()
        await repository.save_subscription(subscription)
