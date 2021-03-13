from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

import pydantic
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship


class UserData(pydantic.BaseModel):
    email: str
    user_id: int


class SubscriptionState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"
    NOT_CREATED = "not-created"

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class Subscription:
    user_id: int
    creation_date: datetime
    state: SubscriptionState
    # is_for_life: bool
    stripe_session_id: Optional[str] = ""
    due_date: Optional[datetime] = None
    stripe_id: Optional[str] = ""
    stripe_customer_id: Optional[str] = ""


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
    Column("stripe_id", String(128), nullable=True),
    Column("stripe_customer_id", String(128), nullable=False),
    Column("stripe_session_id", String(128), nullable=False),
    Column("state", String(16), nullable=False),
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
        )
    },
)
