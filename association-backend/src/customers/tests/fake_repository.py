from typing import Optional

from src.customers.domain.entities import Customer, UserID


class FakeCustomersRepository:
    def __init__(self, customers: Optional[list[Customer]] = None) -> None:
        customers = customers or []

        self._id_counter = max([c.id for c in customers]) + 1 if customers else 0
        self._CUSTOMERS_BY_USER_ID = {
            customer.user_id: customer for customer in customers
        }
        self._CUSTOMERS_BY_STRIPE_CUSTOMER_ID = {
            customer.stripe_customer_id: customer for customer in customers
        }

    async def get_for_user_id(self, user_id: UserID) -> Optional[Customer]:
        return self._CUSTOMERS_BY_USER_ID.get(user_id, None)

    async def get_for_stripe_customer_id(
        self, stripe_customer_id: str
    ) -> Optional[Customer]:
        return self._CUSTOMERS_BY_STRIPE_CUSTOMER_ID.get(stripe_customer_id, None)

    async def create_for_user(self, user_id: UserID, email: str) -> Customer:
        self._id_counter = self._id_counter + 1

        stripe_customer_id = f"cus_test_{user_id}"
        customer = Customer(
            id=self._id_counter, user_id=user_id, stripe_customer_id=stripe_customer_id
        )
        self._CUSTOMERS_BY_USER_ID[user_id] = customer
        self._CUSTOMERS_BY_STRIPE_CUSTOMER_ID[stripe_customer_id] = customer
        return customer

    async def create_stripe_portal_session_url(self, customer: Customer) -> str:
        return f"https://fake.stripe/customerportal/{customer.stripe_customer_id}"
