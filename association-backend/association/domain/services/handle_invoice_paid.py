# import logging
# from datetime import datetime

# from pydantic import BaseModel

# from association_membership.domain.entities import SubscriptionPayment
# from association_membership.domain.repository import AssociationmembershipRepository
# from association.domain.exceptions import SubscriptionNotFound

# logger = logging.getLogger(__name__)


# class InvoicePaidInput(BaseModel):
#     invoice_id: str
#     subscription_id: str
#     paid_at: datetime
#     invoice_pdf: str


# async def handle_invoice_paid(
#     invoice_input: InvoicePaidInput, association_repository: AssociationmembershipRepository
# ):
#     subscription = (
#         await association_repository.get_subscription_by_stripe_subscription_id(
#             invoice_input.subscription_id
#         )
#     )
#     if subscription:
#         payment = await association_repository.get_payment_by_stripe_invoice_id(
#             invoice_input.invoice_id
#         )
#         if not payment:
#             payment = SubscriptionPayment(
#                 payment_date=invoice_input.paid_at,
#                 subscription=subscription,
#                 stripe_invoice_id=invoice_input.invoice_id,
#                 invoice_pdf=invoice_input.invoice_pdf,
#             )
#             await association_repository.save_payment(payment)
#             await association_repository.commit()
#             return subscription
#         else:
#             logger.debug("Payment already registered")
#     else:
#         msg = f"No Subscription found with subscription_id:{invoice_input.subscription_id}"
#         logger.warning(msg)
#         raise SubscriptionNotFound(msg)
