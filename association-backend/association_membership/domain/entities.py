from __future__ import annotations

import logging
from datetime import datetime
from enum import Enum
from typing import Any, List

import ormar
import pydantic
from pydantic import PrivateAttr

from association.domain.entities.stripe import (
    StripeSubscription,
    StripeSubscriptionStatus,
)
from association.domain.exceptions import InconsistentStateTransitionError
from customers.domain.entities import Customer
from database.db import BaseMeta

# from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
# from sqlalchemy.orm import registry, relationship

logger = logging.getLogger(__name__)


class UserData(pydantic.BaseModel):
    email: str
    user_id: int


class SubscriptionStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELED = "canceled"

    def __str__(self) -> str:
        return str.__str__(self)


class Subscription(ormar.Model):
    class Meta(BaseMeta):
        tablename = "subscriptions"

    id: int = ormar.Integer(primary_key=True)
    customer: Customer = ormar.ForeignKey(Customer)
    stripe_subscription_id: str = ormar.String(nullable=False, max_length=256)
    status: SubscriptionStatus = ormar.String(
        max_length=20, choices=list(SubscriptionStatus)
    )

    _add_invoice: List[SubscriptionInvoice] = PrivateAttr(default_factory=list)
    # state: str = ormar.String(max_length=200)
    # created_at: datetime = ormar.DateTime()
    # TODO Is available a auto_update_now?
    # modified_at: Optional[datetime] = ormar.DateTime(
    #     required=False, nullable=True, default=None, server_default=None
    # )
    # # stripe_customer_id: Optional[str] = ""
    # canceled_at: Optional[datetime] = ormar.DateTime(
    #     required=False, nullable=True, default=None, server_default=None
    # )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._add_invoice = []

    def add_invoice(self, payment: SubscriptionInvoice):
        self._add_invoice.append(payment)

    def mark_as_canceled(self):
        self._change_state(SubscriptionStatus.CANCELED)

    def mark_as_active(self):
        self._change_state(SubscriptionStatus.ACTIVE)

    def _change_state(self, to: SubscriptionStatus):
        logger.info("Switching subscription from status %s to %s", self.status, to)
        self.status = to

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
            self.state = SubscriptionStatus.ACTIVE
        elif stripe_subscription.status == StripeSubscriptionStatus.INCOMPLETE:
            self.state = SubscriptionStatus.PENDING
        elif stripe_subscription.status == StripeSubscriptionStatus.INCOMPLETE_EXPIRED:
            if self.state in [
                SubscriptionStatus.ACTIVE,
                SubscriptionStatus.EXPIRED,
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
            self.state = SubscriptionStatus.PENDING
            # the User cannot access the old Subscription
            self.stripe_subscription_id = ""
        elif stripe_subscription.status in [
            StripeSubscriptionStatus.CANCELED,
            StripeSubscriptionStatus.UNPAID,
        ]:
            self.state = SubscriptionStatus.CANCELED
            # the User cannot access the old Subscription
            self.stripe_subscription_id = ""
        else:
            # This is not a terminal state because User can change his payment settings going to customer portal
            self.state = SubscriptionStatus.EXPIRED

        # Update Dates
        self.canceled_at = stripe_subscription.canceled_at
        self.modified_at = datetime.now()

        logger.debug(f"updated subscription {self}")
        return self


class PaymentStatus(str, Enum):
    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    UNCOLLECTIBLE = "uncollectible"
    VOID = "void"

    def __str__(self) -> str:
        return str.__str__(self)


class SubscriptionInvoice(ormar.Model):
    class Meta(BaseMeta):
        tablename = "subscription_invoices"

    id: int = ormar.Integer(primary_key=True)
    status: PaymentStatus = ormar.String(
        max_length=50,
        default=PaymentStatus.DRAFT,
        server_default=PaymentStatus.DRAFT,
        choices=list(PaymentStatus),
    )
    subscription: Subscription = ormar.ForeignKey(Subscription)
    payment_date: datetime = ormar.DateTime()
    period_start: datetime = ormar.DateTime()
    period_end: datetime = ormar.DateTime()
    stripe_invoice_id: str = ormar.String(max_length=256)
    invoice_pdf: str = ormar.Text()
