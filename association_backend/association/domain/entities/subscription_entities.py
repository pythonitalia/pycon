from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.orm import registry


@dataclass
class SubscriptionRequest:
    user_id: str
    request_date: datetime
    stripe_session_id: str
    stripe_subscription_id: Optional[str] = ""
    stripe_customer_id: Optional[str] = ""


@dataclass
class Subscription:
    user_id: str
    payment_date: datetime
    stripe_id: str
    stripe_customer_id: str


mapper_registry = registry()

# =============

subscriptionrequest_table = Table(
    "SubscriptionRequest",
    mapper_registry.metadata,
    Column("user_id", String(32), nullable=False),
    Column("request_date", DateTime(timezone=True), nullable=False, primary_key=True),
    Column("stripe_session_id", String(128), nullable=False, primary_key=True),
    Column("stripe_subscription_id", String(128), nullable=False),
    Column("stripe_customer_id", String(128), nullable=False),
)

mapper_registry.map_imperatively(SubscriptionRequest, subscriptionrequest_table)

# =============

subscription_table = Table(
    "Subscription",
    mapper_registry.metadata,
    Column("user_id", String(32), nullable=False, primary_key=True),
    Column("payment_date", DateTime(timezone=True), nullable=False, primary_key=True),
    Column("stripe_id", String(128), nullable=False, unique=True),
    Column("stripe_customer_id", String(128), nullable=False),
)

mapper_registry.map_imperatively(Subscription, subscription_table)
