from __future__ import annotations

import logging
from datetime import datetime
from enum import Enum
from typing import Any, List, Union

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

    _payments_to_add: List[
        Union[StripeSubscriptionPayment, PretixPayment]
    ] = PrivateAttr(default_factory=list)

    def mark_as_canceled(self):
        self._change_state(SubscriptionStatus.CANCELED)

    def mark_as_active(self):
        self._change_state(SubscriptionStatus.ACTIVE)

    @property
    def is_active(self) -> bool:
        return self.status == SubscriptionStatus.ACTIVE

    def _change_state(self, to: SubscriptionStatus):
        logger.info(
            "Switching subscription_id=%s of user_id=%s from status %s to %s",
            self.id,
            self.user_id,
            self.status,
            to,
        )
        self.status = to

    def add_pretix_payment(
        self,
        *,
        organizer: str,
        event: str,
        order_code: str,
        total: int,
        status: PaymentStatus,
        payment_date: datetime,
        period_start: datetime,
        period_end: datetime,
    ):
        self._payments_to_add.append(
            PretixPayment(
                payment=Payment(
                    idempotency_key=PretixPayment.generate_idempotency_key(
                        organizer, event, order_code
                    ),
                    total=total,
                    status=status,
                    payment_date=payment_date,
                    period_start=period_start,
                    period_end=period_end,
                    subscription=self.id,
                ),
                order_code=order_code,
                event_organizer=organizer,
                event_id=event,
            )
        )

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
        self._payments_to_add.append(
            StripeSubscriptionPayment(
                payment=Payment(
                    idempotency_key=stripe_invoice_id,
                    total=total,
                    status=status,
                    payment_date=payment_date,
                    period_start=period_start,
                    period_end=period_end,
                    subscription=self.id,
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
    subscription: Subscription = ormar.ForeignKey(Subscription, nullable=False)
    # idempotency_key is used as a generic method to keep track of "already handled payments"
    # if a payment comes with the same idempotency_key it gets rejected
    idempotency_key: str = ormar.String(max_length=256, nullable=False, unique=True)
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
    event_organizer: str = ormar.String(max_length=512)
    event_id: str = ormar.String(max_length=512)

    @staticmethod
    def generate_idempotency_key(organizer: str, event: str, order_code: str) -> str:
        return f"{organizer}_{event}_{order_code}"


class StripeSubscriptionPayment(ormar.Model):
    class Meta(BaseMeta):
        tablename = "stripe_subscription_payments"

    id: int = ormar.Integer(primary_key=True)
    payment: Payment = ormar.ForeignKey(Payment, nullable=False)
    stripe_subscription_id: str = ormar.String(max_length=256)
    stripe_invoice_id: str = ormar.String(max_length=256, unique=True)
    invoice_pdf: str = ormar.Text()


class StripeCustomer(ormar.Model):
    class Meta(BaseMeta):
        tablename = "stripe_customers"

    id: int = ormar.Integer(primary_key=True)
    user_id: int = ormar.Integer(unique=True)
    stripe_customer_id: str = ormar.String(max_length=256, unique=True)
