import logging

import ormar
import stripe

from customers.domain.entities import Customer, UserID

logger = logging.getLogger(__name__)


class CustomersRepository:
    async def get_for_user_id(self, user_id: UserID) -> Customer:
        try:
            return await Customer.objects.get(user_id=user_id)
        except ormar.NoMatch:
            return None

    async def create_for_user(self, user_id: UserID, email: str) -> Customer:
        customers = stripe.Customer.list(email=email)

        if len(customers.data) > 1:
            logger.error(
                f"While trying to create a Stripe customer for user_id {user_id}"
                " we found multiple Stripe customers with the same email, investigate this"
            )
            raise ValueError("Multiple customers found")
            # raise MultipleCustomerReturned()

        stripe_customer = customers.data[0] if customers.data else None

        if not stripe_customer:
            stripe_customer = stripe.Customer.create(
                email=email, metadata={"user_id": user_id}
            )

        customer = await Customer.objects.create(
            user_id=user_id, stripe_customer_id=stripe_customer.id
        )

        return customer
