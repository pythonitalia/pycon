from dataclasses import dataclass
from typing import Optional

from pydantic import validator
from pydantic.main import BaseModel


@dataclass
class StripeCustomer:
    id: str
    email: str


@dataclass
class StripeCheckoutSession:
    id: str
    customer_id: Optional[str] = ""
    subscription_id: Optional[str] = ""


class StripeCheckoutSessionInput(BaseModel):
    customer_id: Optional[str] = None
    customer_email: Optional[str] = None

    @validator("customer_email")
    def check_customer_id_or_customer_email(cls, customer_email, values):
        if not values.get("customer_id") and not customer_email:
            raise ValueError("either customer_id or customer_email is required")
        return customer_email
