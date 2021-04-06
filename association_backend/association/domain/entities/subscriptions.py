from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

import pydantic
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from association.domain.entities.stripe import (
    StripeSubscription,
    StripeSubscriptionStatus,
)
from association.domain.exceptions import InconsistentStateTransitionError

logger = logging.getLogger(__name__)


class UserData(pydantic.BaseModel):
    email: str
    user_id: int


class SubscriptionState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELED = "canceled"

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class Subscription:
    user_id: int
    state: SubscriptionState
    created_at: datetime
    # TODO Is available a auto_update_now?
    modified_at: Optional[datetime] = None
    # TODO ADD me
    # last_payed_at : Optional[datetime] = None
    # TODO ADD me
    # active_until : Optional[datetime] = None
    # is_for_life: bool = False
    stripe_subscription_id: Optional[str] = ""
    stripe_customer_id: Optional[str] = ""
    canceled_at: Optional[datetime] = None

    def sync_with_stripe_subscription(
        self, stripe_subscription: StripeSubscription
    ) -> Subscription:
        """ TODO Test ME """
        # Update Customer
        if stripe_subscription.customer_id:
            self.customer_id = stripe_subscription.customer_id

        # Update Subscription
        if stripe_subscription.id:
            self.stripe_subscription_id = stripe_subscription.id

        # Update status
        if stripe_subscription.status == StripeSubscriptionStatus.ACTIVE:
            self.state = SubscriptionState.ACTIVE
        elif stripe_subscription.status == StripeSubscriptionStatus.INCOMPLETE:
            self.state = SubscriptionState.PENDING
        elif stripe_subscription.status == StripeSubscriptionStatus.INCOMPLETE_EXPIRED:
            if self.state in [
                SubscriptionState.ACTIVE,
                SubscriptionState.EXPIRED,
            ]:
                error_message = (
                    "This should not happen...the state INCOMPLETE_EXPIRED should be associated to"
                    "a subscription with status PENDING"
                )
                raise InconsistentStateTransitionError(error_message)
            if len(self.subscription_payments):
                error_message = (
                    "This should not happen...the state INCOMPLETE_EXPIRED should be associated to"
                    "a subscription without associated Payments"
                )
                raise InconsistentStateTransitionError(error_message)
            self.state = SubscriptionState.PENDING
            # the User cannot access the old Subscription
            self.stripe_subscription_id = ""
        elif stripe_subscription.status in [
            StripeSubscriptionStatus.CANCELED,
            StripeSubscriptionStatus.UNPAID,
        ]:
            self.state = SubscriptionState.CANCELED
            # the User cannot access the old Subscription
            self.stripe_subscription_id = ""
        else:
            # This is not a terminal state because User can change his payment settings going to customer portal
            self.state = SubscriptionState.EXPIRED

        # Update Dates
        self.canceled_at = stripe_subscription.canceled_at
        self.modified_at = datetime.now()

        logger.debug(f"updated subscription {self}")
        return self


@dataclass
class SubscriptionPayment:
    subscription: Subscription
    payment_date: datetime
    stripe_invoice_id: str
    invoice_pdf: str


mapper_registry = registry()

subscription_table = Table(
    "subscription",
    mapper_registry.metadata,
    Column("user_id", Integer(), nullable=False, primary_key=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("modified_at", DateTime(timezone=True), nullable=False),
    Column("stripe_subscription_id", String(128), nullable=True),
    Column("stripe_customer_id", String(128), nullable=False),
    Column("state", String(24), nullable=False),
    Column("canceled_at", DateTime(timezone=True), nullable=True),
)

subscription_payment_table = Table(
    "subscription_payment",
    mapper_registry.metadata,
    Column("stripe_invoice_id", String(128), nullable=False, primary_key=True),
    Column(
        "subscription_id", Integer, ForeignKey("subscription.user_id"), nullable=False
    ),
    Column("payment_date", DateTime(timezone=True), nullable=False),
    Column("invoice_pdf", String(128), nullable=True),
)

mapper_registry.map_imperatively(Subscription, subscription_table)
mapper_registry.map_imperatively(
    SubscriptionPayment,
    subscription_payment_table,
    properties={
        "subscription": relationship(
            Subscription,
            backref="subscription_payments",
        )
    },
)
