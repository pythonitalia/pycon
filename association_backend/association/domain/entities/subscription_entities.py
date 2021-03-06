from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.orm import registry

rome_tz = ZoneInfo("Europe/Rome")


@dataclass
class UserData:
    email: str
    user_id: int


class SubscriptionState(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class Subscription:
    user_id: int
    creation_date: datetime
    state: SubscriptionState
    stripe_session_id: Optional[str] = ""
    payment_date: Optional[datetime] = None
    stripe_id: Optional[str] = ""
    stripe_customer_id: Optional[str] = ""
    expiration_date: Optional[datetime] = None

    def is_paid(self):
        return self.payment_date is not None

    def is_expired(self):
        return (
            self.payment_date
            and self.payment_date < datetime.now(rome_tz) - relativedelta(years=1)
            or False
        )

    def get_calculated_state(self) -> SubscriptionState:
        """
        This method will be called by a cron (https://github.com/encode/starlette/issues/915#issuecomment-622945864)
        to set the field "state"
        :return:
        """
        if not self.payment_date:
            return SubscriptionState.PENDING
        elif self.payment_date < datetime.now(rome_tz) - relativedelta(years=1):
            return SubscriptionState.EXPIRED
        else:
            return SubscriptionState.ACTIVE


mapper_registry = registry()

# =============

subscription_table = Table(
    "Subscription",
    mapper_registry.metadata,
    Column("user_id", Integer(), nullable=False, primary_key=True),
    Column("creation_date", DateTime(timezone=True), nullable=False),
    Column("payment_date", DateTime(timezone=True), nullable=True),
    Column("stripe_id", String(128), nullable=True),
    Column("stripe_customer_id", String(128), nullable=False),
    Column("stripe_session_id", String(128), nullable=False),
    Column("state", String(16), nullable=False),
    Column("expiration_date", DateTime(timezone=True), nullable=True),
)

mapper_registry.map_imperatively(Subscription, subscription_table)
