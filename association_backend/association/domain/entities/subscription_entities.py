from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from zoneinfo import ZoneInfo

import pydantic
from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

rome_tz = ZoneInfo("Europe/Rome")


class UserData(pydantic.BaseModel):
    email: str
    user_id: int


class SubscriptionState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"
    PAYMENT_FAILED = "payment-failed"

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class Subscription:
    user_id: int
    creation_date: datetime
    state: SubscriptionState
    stripe_session_id: Optional[str] = ""
    due_date: Optional[datetime] = None
    stripe_id: Optional[str] = ""
    stripe_customer_id: Optional[str] = ""
    expiration_date: Optional[datetime] = None

    def get_calculated_state(self) -> SubscriptionState:
        """
        This method will be called by a cron (https://github.com/encode/starlette/issues/915#issuecomment-622945864)
        to set the field "state"
        :return:
        """
        if not self.due_date:
            return SubscriptionState.PENDING
        elif self.due_date < datetime.now(rome_tz) - relativedelta(years=1):
            return SubscriptionState.EXPIRED
        else:
            return SubscriptionState.ACTIVE


@dataclass
class SubscriptionPayment:
    subscription: Subscription
    payment_date: datetime
    invoice_id: str
    invoice_pdf: str


# =============
mapper_registry = registry()

subscription_table = Table(
    "subscription",
    mapper_registry.metadata,
    Column("user_id", Integer(), nullable=False, primary_key=True),
    Column("creation_date", DateTime(timezone=True), nullable=False),
    Column("next_payment_due_date", DateTime(timezone=True), nullable=True),
    Column("stripe_id", String(128), nullable=True),
    Column("stripe_customer_id", String(128), nullable=False),
    Column("stripe_session_id", String(128), nullable=False),
    Column("state", String(16), nullable=False),
    Column("expiration_date", DateTime(timezone=True), nullable=True),
)

subscription_payment_table = Table(
    "subscription_payment",
    mapper_registry.metadata,
    Column("invoice_id", String(128), nullable=False, primary_key=True),
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
            # order_by=address.c.id
        )
    },
)
