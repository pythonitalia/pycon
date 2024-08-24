import logging

import requests
from notifications.permissions import IsSNSAuthenticated, SNSAuthentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([IsSNSAuthenticated])
@authentication_classes([SNSAuthentication])
def sns_webhook(request):
    payload = request.data
    message_type = request.headers.get("x-amz-sns-message-type")

    logger.info(f"Received SNS message of type {message_type}")

    if message_type == "SubscriptionConfirmation":
        subscribe_url = payload["SubscribeURL"]
        requests.get(subscribe_url)
        return Response(status=200)

    if message_type == "Notification":
        # Process the notification
        return Response(status=200)

    return Response(status=200)
