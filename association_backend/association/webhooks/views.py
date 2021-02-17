import logging
from typing import cast

import stripe
from association.db import get_engine, get_session
from association.domain import services
from association.domain.repositories import AssociationRepository
from association.domain.services import SubscriptionInputModel, SubscriptionUpdateInput
from association.domain.services.exceptions import (
    SubscriptionNotCreated,
    SubscriptionNotUpdated,
)
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

    async def handle_customer_subscription_created(self, request, payload):
        stripe_obj = payload["object"]
        try:
            await services.set_subscription_payed(
                SubscriptionInputModel(subscription_id=stripe_obj["id"]),
                association_repository=self._get_association_repository(request),
            )
            return JSONResponse({"event": payload.get("type", ""), "msg": "OK"})
        except SubscriptionNotCreated as ex:
            return JSONResponse(
                {"event": payload.get("type", ""), "msg": "KO", "error": str(ex)}
            )

    async def handle_checkout_session_completed(self, request, payload):
        stripe_obj = payload["object"]
        try:
            await services.update_draft_subscription(
                SubscriptionUpdateInput(
                    session_id=stripe_obj["id"],
                    customer_id=stripe_obj["customer"],
                    subscription_id=stripe_obj["subscription"],
                ),
                association_repository=self._get_association_repository(request),
            )
            return JSONResponse({"event": payload.get("type", ""), "msg": "OK"})
        except SubscriptionNotUpdated as ex:
            return JSONResponse(
                {"event": payload.get("type", ""), "msg": "KO", "error": str(ex)}
            )

    async def handle_customer_subscription_updated(self, request, payload):
        logger.debug(payload)
        return JSONResponse({"event": payload.get("type", ""), "msg": "OK"})

    async def handle_payout_paid(self, request, payload):
        return JSONResponse({"event": payload.get("type", ""), "msg": "KO"})

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
            message = await self.echo(data)
            resp = {"data": {}, "event": event_type, "message": message}
        elif event_type == "invoice.payment_failed":
            # The payment failed or the customer does not have a valid payment method.
            # The subscription becomes past_due. Notify your customer and send them to the
            # customer portal to update their payment information.
            message = await self.echo(data)
            resp = {"data": {}, "event": event_type, "message": message}
        elif event_type == "customer.subscription.created":
            return await self.handle_customer_subscription_created(request, data)
        elif event_type == "customer.subscription.updated":
            message = await self.echo(data)
            resp = {"data": {}, "event": event_type, "message": message}
        else:
            logger.warning(
                f"The event `{event_type}` is not handled by webhook",
                extra={"tags": event, "payload": data},
            )
            message = await self.echo(data)
            resp = {"data": {}, "event": event_type, "message": message}

        return JSONResponse(resp)

    async def echo(self, payload):
        return f"got object `{payload['object']}`"
