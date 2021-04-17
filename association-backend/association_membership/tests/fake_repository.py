class FakeAssociationMembershipRepository:
    async def create_checkout_session(self, customer_id: str) -> str:
        return f"cs_session_{customer_id}"
