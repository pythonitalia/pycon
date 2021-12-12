# import logging
# from typing import Optional

# import stripe

# from src.customers.domain.entities import Customer, UserID

# logger = logging.getLogger(__name__)


# class CustomersRepository:
#     async def get_for_user_id(self, user_id: UserID) -> Optional[Customer]:
#         return await Customer.objects.select_related("subscriptions").get_or_none(
#             user_id=user_id
#         )

#     async def get_for_stripe_customer_id(
#         self, stripe_customer_id: str
#     ) -> Optional[Customer]:
#         return await Customer.objects.select_related("subscriptions").get_or_none(
#             stripe_customer_id=stripe_customer_id
#         )

#     async def create_for_user(self, user_id: UserID, email: str) -> Customer:
#         stripe_customer = stripe.Customer.create(
#             email=email, metadata={"user_id": user_id}
#         )

#         customer = await Customer.objects.create(
#             user_id=user_id, stripe_customer_id=stripe_customer.id
#         )

#         return customer

#     async def create_stripe_portal_session_url(self, customer: Customer) -> str:
#         session = stripe.billing_portal.Session.create(
#             customer=customer.stripe_customer_id
#         )
#         return session.url
