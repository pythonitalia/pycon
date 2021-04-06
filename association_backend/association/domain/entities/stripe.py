from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class StripeSubscriptionStatus(str, Enum):
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"
    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"

    def __str__(self) -> str:
        return str.__str__(self)


@dataclass
class StripeCustomer:
    id: str
    email: str


@dataclass
class StripeCheckoutSession:
    id: str
    customer_id: Optional[str] = ""
    subscription_id: Optional[str] = ""


@dataclass
class StripeSubscription:
    id: str
    status: StripeSubscriptionStatus
    customer_id: str
    canceled_at: Optional[datetime] = None
