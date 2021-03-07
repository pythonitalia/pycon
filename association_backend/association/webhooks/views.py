import logging
from typing import cast

import stripe
from association.db import get_engine, get_session
from association.domain import services
from association.domain.exceptions import SubscriptionNotFound, SubscriptionNotUpdated
from association.domain.repositories import AssociationRepository
from association.settings import STRIPE_WEBHOOK_SIGNATURE_SECRET
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


class StripeWebhook(HTTPEndpoint):
    """
    https://stripe.com/docs/billing/subscriptions/checkout#webhooks
    """

    def _get_association_repository(self, request):
        return AssociationRepository(
            session=cast(AsyncSession, get_session(get_engine(echo=False)))
        )  # session=AsyncSession

    async def handle_checkout_session_completed(self, request, payload):
        stripe_obj = payload["object"]
        try:
            await services.update_pending_subscription(
                services.SubscriptionUpdateInput(
                    session_id=stripe_obj["id"],
                    customer_id=stripe_obj["customer"],
                    subscription_id=stripe_obj["subscription"],
                ),
                association_repository=self._get_association_repository(request),
            )
            return JSONResponse({"status": "success"})
        except SubscriptionNotUpdated:
            return JSONResponse({"status": "error"}, status_code=400)

    async def handle_customer_subscription_updated(self, request, payload):
        stripe_obj = payload["object"]
        try:
            await services.handle_customer_subscription_updated(
                services.SubscriptionDetailInput(
                    subscription_id=stripe_obj["id"],
                    status=stripe_obj["status"],
                    current_period_start=stripe_obj["current_period_start"],
                    current_period_end=stripe_obj["current_period_end"],
                    latest_invoice=stripe_obj["latest_invoice"],
                ),
                association_repository=self._get_association_repository(request),
            )
            return JSONResponse({"status": "success"})
        except SubscriptionNotUpdated:
            return JSONResponse({"status": "error"}, status_code=400)

    async def handle_invoice_paid(self, request, payload):
        """ https://stripe.com/docs/api/invoices/object?lang=python """
        stripe_obj = payload["object"]
        try:
            await services.handle_invoice_paid(
                services.InvoicePaidInput(
                    invoice_id=stripe_obj["id"],
                    subscription_id=stripe_obj["subscription"],
                    paid_at=stripe_obj["status_transitions"]["paid_at"],
                    invoice_pdf=stripe_obj["invoice_pdf"],
                ),
                association_repository=self._get_association_repository(request),
            )
            return JSONResponse({"status": "success"})
        except SubscriptionNotFound:
            return JSONResponse({"status": "error"}, status_code=400)

    async def handle_invoice_payment_failed(self, request, payload):
        """ https://stripe.com/docs/api/invoices/object?lang=python """
        stripe_obj = payload["object"]
        # object : https://stripe.com/docs/api/invoices/object?lang=python
        try:
            await services.handle_invoice_payment_failed(
                services.InvoicePaymentFailedInput(
                    invoice_id=stripe_obj["id"],
                    subscription_id=stripe_obj["subcription"],
                    paid_at=stripe_obj["status_transitions"]["paid_at"],
                    invoice_pdf=stripe_obj["invoice_pdf"],
                ),
                association_repository=self._get_association_repository(request),
            )
            return JSONResponse({"status": "success"})
        except SubscriptionNotFound:
            return JSONResponse({"status": "error"}, status_code=400)

    async def post(self, request):
        webhook_secret = STRIPE_WEBHOOK_SIGNATURE_SECRET
        request_data = await request.body()
        logger.debug(f"request_data : {request_data}")

        if webhook_secret:
            # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            signature = request.headers.get("stripe-signature")
            logger.debug(f"signature : {signature}")
            try:
                event = stripe.Webhook.construct_event(
                    payload=request_data, sig_header=signature, secret=webhook_secret
                )
                data = event["data"]
            except Exception as e:
                logger.exception(str(e))
                raise e
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event["type"]
        else:
            data = request_data["data"]
            event_type = request_data["type"]
        print(f"Handling event {event_type}")
        # await self.echo(data)
        # print(await request.json())
        # data_object = data['object']

        if event_type == "checkout.session.completed":
            # Payment is successful and the subscription is created.
            # You should provision the subscription.
            return await self.handle_checkout_session_completed(request, data)
        elif event_type == "invoice.paid":
            # Continue to provision the subscription as payments continue to be made.
            # Store the status in your database and check when a user accesses your service.
            # This approach helps you avoid hitting rate limits.
            return await self.handle_invoice_paid(request, data)
        # elif event_type == "invoice.payment_succeeded":
        #     # Continue to provision the subscription as payments continue to be made.
        #     # Store the status in your database and check when a user accesses your service.
        #     # This approach helps you avoid hitting rate limits.
        #     return await self.handle_invoice_paid(request, data)
        elif event_type == "invoice.payment_failed":
            # The payment failed or the customer does not have a valid payment method.
            # The subscription becomes past_due. Notify your customer and send them to the
            # customer portal to update their payment information.
            return await self.handle_invoice_payment_failed(data)
        elif event_type == "customer.subscription.updated":
            # TODO ENABLE ME
            # return await self.handle_customer_subscription_updated(request, data)
            pass
        else:
            logger.warning(
                f"The event `{event_type}` is not handled by webhook",
                extra={"tags": event, "payload": data},
            )

        return JSONResponse({"status": "success"})

    async def echo(self, payload):
        print(f"got object `{payload['object']}`")
