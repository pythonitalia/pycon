from typing import Optional

from pydantic.main import BaseModel


class StripeCustomer(BaseModel):
    id: str


class StripeCheckoutSession(BaseModel):
    id: str
    customer_id: Optional[str] = ""
