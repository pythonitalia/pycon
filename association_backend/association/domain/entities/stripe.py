from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import validator
from pydantic.main import BaseModel


class StripeStatus(str, Enum):
    # TODO RENAME IN StripeSubscriptionStatus
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
    status: StripeStatus
    customer_id: str
    canceled_at: Optional[datetime] = None


class StripeCheckoutSessionInput(BaseModel):
    customer_id: Optional[str] = None
    customer_email: Optional[str] = None

    @validator("customer_email")
    def check_customer_id_or_customer_email(cls, customer_email, values):
        if not values.get("customer_id") and not customer_email:
            raise ValueError("either customer_id or customer_email is required")
        return customer_email
