from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.orm import registry

# @dataclass
# class Subscription:
#     user_id: str
#     request_date: datetime
#     stripe_session_id: str
#     stripe_subscription_id: Optional[str] = ""
#     stripe_customer_id: Optional[str] = ""


class SubscriptionState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class Subscription:
    user_id: str
    creation_date: datetime
    stripe_session_id: str
    state: SubscriptionState
    payment_date: Optional[datetime] = None
    stripe_id: Optional[str] = ""
    stripe_customer_id: Optional[str] = ""


mapper_registry = registry()

# =============

subscription_table = Table(
    "Subscription",
    mapper_registry.metadata,
    Column("user_id", String(32), nullable=False, primary_key=True),
    Column("creation_date", DateTime(timezone=True), nullable=False),
    Column("payment_date", DateTime(timezone=True), nullable=True),
    Column("stripe_id", String(128), nullable=True),
    Column("stripe_customer_id", String(128), nullable=False),
    Column("stripe_session_id", String(128), nullable=False, primary_key=True),
    Column("state", String(16), nullable=False),
)

mapper_registry.map_imperatively(Subscription, subscription_table)
