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

    subscriber = get_subscriber(email)

    if not subscriber:
        return subscribe_email(email, ip)

    email_status = subscriber.get("status")
    segments = subscriber.get("segments")

    if email_status == "active":
        if not is_in_segment(segments):
            # if the user is added to our flodesk audience
            # but not to the segment of this integration, we add them
            add_to_segment(email, settings.FLODESK_SEGMENT_ID)

        return SubscriptionResult.SUBSCRIBED

    if email_status == "bounced":
        return SubscriptionResult.UNABLE_TO_SUBSCRIBE

    if email_status == "unconfirmed":
        return SubscriptionResult.WAITING_CONFIRMATION

    if email_status and email_status in OPT_IN_REQUIRED_STATUSES:
        # we can't automatically subscribe them again via API.
        # flodesk requires us to redirect them to a hosted opt-in form
        return SubscriptionResult.OPT_IN_FORM_REQUIRED


def is_in_segment(segments: list[dict[str, any]]) -> bool:
    return any(segment["id"] == settings.FLODESK_SEGMENT_ID for segment in segments)


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

    add_to_segment(raw_email, settings.FLODESK_SEGMENT_ID)

    return SubscriptionResult.SUBSCRIBED


def add_to_segment(email: str, segment_id: str) -> None:
    response = call_flodesk_api(
        f"subscribers/{email}/segments",
        "POST",
        json={"segment_ids": [segment_id]},
    )

    response.raise_for_status()


def get_subscriber(email: str):
    response = call_flodesk_api(f"subscribers/{email}", "GET")

    try:
        response.raise_for_status()
    except HTTPError:
        # If the request fails, assume it is because of a 404
        # or similar. If flodesk is down we will fail later anyway
        return None

    data = response.json()
    return data


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
