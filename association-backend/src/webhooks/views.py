import logging

import stripe
from starlette.responses import Response

from src.association.settings import STRIPE_WEBHOOK_SECRET
from src.webhooks.exceptions import WebhookError
from src.webhooks.handlers import HANDLERS

logger = logging.getLogger(__file__)


async def stripe_webhook(request):
    payload = await request.body()

    try:
        signature = request.headers.get("stripe-signature")
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=signature, secret=str(STRIPE_WEBHOOK_SECRET)
        )
    except ValueError as e:
        logger.exception("Called stripe webhook but parsing failed!", exc_info=e)
        raise
    except stripe.error.SignatureVerificationError as e:
        logger.exception(
            "Called stripe webhook but signature validation failed!", exc_info=e
        )
        raise

    event_type = event["type"]
    handler = HANDLERS.get(event_type, None)

    if not handler:
        logger.info("No handler found for stripe_event=%s", event_type)
        return Response(None, 204)

    logger.info("Running handler for stripe_event=%s", event_type)
    try:
        await handler(event)
    except WebhookError as e:
        logger.exception(
            "Known error while handling stripe_event=%s", event_type, exc_info=e
        )

    return Response(None, 200)
