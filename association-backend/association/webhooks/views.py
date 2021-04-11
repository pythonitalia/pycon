import stripe
from starlette.responses import PlainTextResponse

from association.settings import STRIPE_WEBHOOK_SECRET
from association.webhooks.handlers import HANDLERS


async def stripe_webhook(request):
    payload = await request.body()
    try:
        signature = request.headers.get("stripe-signature")
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=signature, secret=STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        # todo error
        raise
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        # todo
        raise

    handler = HANDLERS.get(event["type"], None)
    print("event type is", event["type"])

    if not handler:
        # TODO: log handler for event not found
        return PlainTextResponse("nope")

    print("run handler:", handler, "for event", event["type"])
    await handler(event)
    return PlainTextResponse("hello")
