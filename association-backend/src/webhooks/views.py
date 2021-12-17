import logging

import stripe
from starlette.responses import Response

from src.association.settings import STRIPE_WEBHOOK_SECRET
from src.webhooks.handlers import run_handler

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
    await run_handler("stripe", event_type, event)
    return Response(None, 200)


async def pretix_webhook(request):
    payload = await request.json()
    action = payload["action"]
    await run_handler("pretix", action, payload)
    return Response(None, 200)
