import logging
import stripe
from django.conf import settings
from association_membership.handlers import run_handler
from association_membership.permissions import (
    IsPretixAuthenticated,
    PretixAuthentication,
)
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response

logger = logging.getLogger(__file__)


@api_view(["POST"])
def stripe_webhook(request):
    try:
        signature = request.headers.get("stripe-signature")
        event = stripe.Webhook.construct_event(
            payload=request.data,
            sig_header=signature,
            secret=settings.STRIPE_WEBHOOK_SECRET,
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
    run_handler("stripe", event_type, event)
    return Response(status=200)


@api_view(["POST"])
@permission_classes([IsPretixAuthenticated])
@authentication_classes([PretixAuthentication])
def pretix_webhook(request):
    payload = request.data
    action = payload["action"]
    run_handler("pretix", action, payload)
    return Response(status=200)
