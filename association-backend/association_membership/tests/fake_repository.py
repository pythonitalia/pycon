from customers.domain.entities import Customer


class FakeAssociationMembershipRepository:
    async def create_checkout_session(self, customer: Customer) -> str:
        return f"cs_session_{customer.stripe_customer_id}"
