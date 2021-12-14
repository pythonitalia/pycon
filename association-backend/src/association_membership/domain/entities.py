from __future__ import annotations

import logging
from datetime import datetime
from enum import Enum
from typing import Any, List

import ormar
import sqlalchemy
from pydantic import PrivateAttr

from src.database.db import BaseMeta

logger = logging.getLogger(__name__)


class DateTimeWithTimeZone(ormar.DateTime):
    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.DateTime(timezone=True)


class SubscriptionStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CANCELED = "canceled"

    def __str__(self) -> str:
        return str.__str__(self)


class PaymentStatus(str, Enum):
    PAID = "paid"
    CANCELED = "canceled"

    def __str__(self) -> str:
        return str.__str__(self)


class Subscription(ormar.Model):
    class Meta(BaseMeta):
        tablename = "subscriptions"

    id: int = ormar.Integer(primary_key=True)
    user_id: int = ormar.Integer(unique=True)
    status: SubscriptionStatus = ormar.String(
        max_length=20,
        choices=list(SubscriptionStatus),
        default=SubscriptionStatus.PENDING,
        nullable=False,
    )

    _add_stripe_subscription_payment: List[StripeSubscriptionPayment] = PrivateAttr(
        default_factory=list
    )

    def mark_as_canceled(self):
        self._change_state(SubscriptionStatus.CANCELED)

    def mark_as_active(self):
        self._change_state(SubscriptionStatus.ACTIVE)

    @property
    def is_active(self) -> bool:
        return self.status == SubscriptionStatus.ACTIVE

    def _change_state(self, to: SubscriptionStatus):
        logger.info("Switching subscription from status %s to %s", self.status, to)
        self.status = to

    def add_stripe_subscription_payment(
        self,
        total: int,
        status: PaymentStatus,
        payment_date: datetime,
        period_start: datetime,
        period_end: datetime,
        stripe_subscription_id: str,
        stripe_invoice_id: str,
        invoice_pdf: str,
    ):
        self._add_stripe_subscription_payment.append(
            StripeSubscriptionPayment(
                payment=Payment(
                    total=total,
                    status=status,
                    payment_date=payment_date,
                    period_start=period_start,
                    period_end=period_end,
                ),
                stripe_subscription_id=stripe_subscription_id,
                stripe_invoice_id=stripe_invoice_id,
                invoice_pdf=invoice_pdf,
            )
        )


class Payment(ormar.Model):
    class Meta(BaseMeta):
        tablename = "payments"

    id: int = ormar.Integer(primary_key=True)
    total: int = ormar.Integer()
    payment_date: datetime = DateTimeWithTimeZone()
    period_start: datetime = DateTimeWithTimeZone()
    period_end: datetime = DateTimeWithTimeZone()
    status: PaymentStatus = ormar.String(
        max_length=20,
        choices=list(PaymentStatus),
        nullable=False,
    )


class PretixPayment(ormar.Model):
    class Meta(BaseMeta):
        tablename = "pretix_payments"

    id: int = ormar.Integer(primary_key=True)
    payment: Payment = ormar.ForeignKey(Payment, nullable=False)
    order_code: str = ormar.String(max_length=256, unique=True)


class StripeSubscriptionPayment(ormar.Model):
    class Meta(BaseMeta):
        tablename = "stripe_subscription_payments"

    id: int = ormar.Integer(primary_key=True)
    payment: Payment = ormar.ForeignKey(Payment, nullable=False)
    stripe_subscription_id: str = ormar.String(max_length=256, unique=True)
    stripe_invoice_id: str = ormar.String(max_length=256, unique=True)
    invoice_pdf: str = ormar.Text()


class StripeCustomer(ormar.Model):
    class Meta(BaseMeta):
        tablename = "stripe_customers"

    id: int = ormar.Integer(primary_key=True)
    user_id: int = ormar.Integer(unique=True)
    stripe_customer_id: str = ormar.String(max_length=256, unique=True)
