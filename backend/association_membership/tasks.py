from pycon.celery import app

import logging
from datetime import datetime, timezone

from association_membership.enums import (
    PaymentStatus,
    MembershipStatus,
)
from association_membership.models import (
    Membership,
)

logger = logging.getLogger(__file__)


@app.task
def check_association_membership_subscriptions():
    update_expired_subscriptions()
    update_now_active_subscriptions()


def update_now_active_subscriptions():
    now = datetime.now(timezone.utc)
    # Ideally in the future we should use the psql NOW() function
    qs = Membership.objects.filter(
        status=MembershipStatus.CANCELED,
        payments__status=PaymentStatus.PAID,
        payments__period_start__lte=now,
        payments__period_end__gte=now,
    )
    subscriptions_to_enable = qs.all()
    subscriptions_to_enable_count = qs.count()

    logger.info(
        "Found subscriptions_to_enable_count=%s subscriptions to activate",
        subscriptions_to_enable_count,
    )

    for subscription in subscriptions_to_enable:
        subscription.mark_as_active()
        subscription.save(update_fields=["status"])


def update_expired_subscriptions():
    now = datetime.now(timezone.utc)

    # Ideally in the future we should use the psql NOW() function
    subscriptions_with_payment_qs = Membership.objects.filter(
        payments__status=PaymentStatus.PAID,
        payments__period_start__lte=now,
        payments__period_end__gte=now,
    )
    subscriptions_with_payment = set(
        subscriptions_with_payment_qs.values_list("id", flat=True)
    )

    qs = Membership.objects.filter(status=MembershipStatus.ACTIVE).exclude(
        payments__status=PaymentStatus.PAID,
        payments__period_start__lte=now,
        payments__period_end__gte=now,
    )

    subscriptions_to_cancel = [
        subscription
        for subscription in qs.all()
        if subscription.id not in subscriptions_with_payment
    ]
    subscriptions_to_cancel_count = len(subscriptions_to_cancel)

    logger.info(
        "Found subscriptions_to_cancel_count=%s subscriptions to cancel",
        subscriptions_to_cancel_count,
    )

    for subscription in subscriptions_to_cancel:
        subscription.mark_as_canceled()
        subscription.save(update_fields=["status"])
