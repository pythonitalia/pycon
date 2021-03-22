import logging
from typing import cast

import stripe
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from association.db import get_engine, get_session
from association.domain import services
from association.domain.exceptions import (
    InconsistentStateTransitionError,
    SubscriptionNotFound,
    WebhookSecretMissing,
)
from association.domain.repositories import AssociationRepository
from association.settings import STRIPE_WEBHOOK_SIGNATURE_SECRET

logger = logging.getLogger(__name__)


class StripeWebhook(HTTPEndpoint):
    """Webhook listening for notification events from stripe account (see https://stripe.com/docs/webhooks and https://stripe.com/docs/billing/subscriptions/checkout#webhooks for more details)
    Required subscribed events (see https://stripe.com/docs/api/events/types for all event types):
      - checkout.session.completed
            Occurs when a Checkout Session has been successfully completed.
            The System expects to receive info about related customer and subscription
      - customer.subscription.updated
            Occurs whenever a subscription changes (e.g., switching from one plan to another, or changing the status from trial to active)
      - invoice.paid
            Occurs whenever an invoice payment attempt succeeds or an invoice is marked as paid out-of-band.
    """

    def _get_association_repository(self, request):
        return AssociationRepository(
            session=cast(AsyncSession, get_session(get_engine(echo=False)))
        )

    async def handle_checkout_session_completed(self, request, stripe_obj):
        try:
            await services.handle_checkout_session_completed(
                services.SubscriptionUpdateInput(
                    session_id=stripe_obj["id"],
                    customer_id=stripe_obj["customer"],
                    subscription_id=stripe_obj["subscription"],
                ),
                association_repository=self._get_association_repository(request),
            )
            return JSONResponse({"status": "success"})
        except SubscriptionNotFound:
            return JSONResponse({"status": "error"}, status_code=400)

    async def handle_customer_subscription_updated(self, request, stripe_obj):
        try:
            await services.update_subscription_from_external_subscription(
                services.SubscriptionDetailInput(
                    subscription_id=stripe_obj["id"],
                    status=stripe_obj["status"],
                    customer_id=stripe_obj["customer"],
                    canceled_at=stripe_obj["canceled_at"],
                ),
                subscription=None,
                association_repository=self._get_association_repository(request),
            )
            return JSONResponse({"status": "success"})
        except SubscriptionNotFound:
            return JSONResponse({"status": "error"}, status_code=400)
        except InconsistentStateTransitionError as ex:
            logger.exception(str(ex))
            return JSONResponse({"status": "error"}, status_code=400)

    async def handle_customer_subscription_deleted(self, request, stripe_obj):
        try:
            await services.update_subscription_from_external_subscription(
                services.SubscriptionDetailInput(
                    subscription_id=stripe_obj["id"],
                    status=stripe_obj["status"],
                    canceled_at=stripe_obj["canceled_at"],
                ),
                subscription=None,
                association_repository=self._get_association_repository(request),
            )
            return JSONResponse({"status": "success"})
        except SubscriptionNotFound:
            return JSONResponse({"status": "error"}, status_code=400)
        except InconsistentStateTransitionError as ex:
            logger.exception(str(ex))
            return JSONResponse({"status": "error"}, status_code=400)

    async def handle_invoice_paid(self, request, stripe_obj):
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
            # # Taken from Stripe example implementation, disabled but maybe useful for test purpose
            # # (see https://github.com/stripe-samples/checkout-single-subscription/blob/master/server/python/server.py)
            # data = request_data["data"]
            # event_type = request_data["type"]
            raise WebhookSecretMissing()
        logger.debug(f"Handling event {event_type}")
        stripe_obj = data["object"]
        if event_type == "checkout.session.completed":
            # Payment is successful and the subscription is created.
            # You should provision the subscription.
            return await self.handle_checkout_session_completed(request, stripe_obj)
        elif event_type == "invoice.paid":
            # Continue to provision the subscription as payments continue to be made.
            # Store the status in your database and check when a user accesses your service.
            # This approach helps you avoid hitting rate limits.
            return await self.handle_invoice_paid(request, stripe_obj)
        elif event_type == "customer.subscription.updated":
            # Every time there is a subscription status update we will be notified
            return await self.handle_customer_subscription_updated(request, stripe_obj)
        elif event_type == "customer.subscription.deleted":
            # Every time there is a subscription status update we will be notified
            return await self.handle_customer_subscription_deleted(request, stripe_obj)

        else:
            logger.warning(
                f"The event `{event_type}` is not handled by webhook."
                f"We should disable it from Stripe panel if unused",
                extra={"tags": event, "payload": stripe_obj},
            )
            await self.echo(data)
            return JSONResponse({"status": "success"})

    async def echo(self, payload):
        print(f"got object `{payload['object']}`")
