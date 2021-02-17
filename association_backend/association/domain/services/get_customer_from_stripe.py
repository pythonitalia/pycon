import logging
from typing import Optional

import stripe
from association.domain.entities.stripe_entities import StripeCustomer
from association.settings import STRIPE_SUBSCRIPTION_API_SECRET
from pydantic import BaseModel, EmailStr

logger = logging.getLogger(__name__)

stripe.api_key = STRIPE_SUBSCRIPTION_API_SECRET  # 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'


class StripeCustomerInput(BaseModel):
    email: EmailStr


async def get_customer_from_stripe(
    data: StripeCustomerInput
) -> Optional[StripeCustomer]:
    # See https://stripe.com/docs/api/....
    customers = stripe.Customer.list(email=data.email)
    if len(customers):
        return StripeCustomer(id=customers.data[0].id)
    else:
        return None
