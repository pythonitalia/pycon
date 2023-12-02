from datetime import datetime
import enum
import logging
from typing import Literal, Optional

import requests
from django.conf import settings
from requests.models import HTTPError, Response

logger = logging.getLogger(__name__)


OPT_IN_REQUIRED_STATUSES = [
    "complained",
    "unsubscribed",
]


class SubscriptionResult(enum.Enum):
    SUBSCRIBED = "subscribed"
    WAITING_CONFIRMATION = "waiting-confirmation"
    UNABLE_TO_SUBSCRIBE = "unable-to-subscribe"
    OPT_IN_FORM_REQUIRED = "opt-in-form-required"


def subscribe(email: str, ip: str) -> SubscriptionResult:
    if not settings.FLODESK_API_KEY:
        raise ValueError("Flodesk integration is not configured")

    email_status = get_email_status(email)

    if email_status == "active":
        # User is already a member, so nothing to do
        return SubscriptionResult.SUBSCRIBED

    if email_status == "bounced":
        return SubscriptionResult.UNABLE_TO_SUBSCRIBE

    if email_status == "unconfirmed":
        return SubscriptionResult.WAITING_CONFIRMATION

    if email_status and email_status in OPT_IN_REQUIRED_STATUSES:
        return SubscriptionResult.OPT_IN_FORM_REQUIRED

    return subscribe_email(email, ip)


def subscribe_email(raw_email: str, ip: str) -> SubscriptionResult:
    response = call_flodesk_api(
        "subscribers",
        "POST",
        json={
            "email": raw_email,
            "optin_ip": ip,
            "optin_timestamp": datetime.now().isoformat(),
        },
    )

    response.raise_for_status()

    return SubscriptionResult.SUBSCRIBED


def get_email_status(email: str) -> Optional[str]:
    response = call_flodesk_api(f"subscribers/{email}", "GET")

    try:
        response.raise_for_status()
    except HTTPError:
        # If the request fails, assume it is because of a 404
        # or similar. If mailchimp is down we will fail later anyway
        return None

    data = response.json()
    return data["status"]


def call_flodesk_api(
    endpoint: str,
    method: Literal["GET", "POST", "PUT"],
    *,
    json: Optional[dict[str, any]] = None,
) -> Response:
    base_url = "https://api.flodesk.com/v1"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {settings.FLODESK_API_KEY}",
    }

    return getattr(requests, method.lower())(
        f"{base_url}/{endpoint}",
        json=json,
        headers=headers,
    )
