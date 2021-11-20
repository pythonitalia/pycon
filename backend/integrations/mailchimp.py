import enum
import hashlib
import logging
from typing import Literal, Optional

import requests
from django.conf import settings
from requests.models import HTTPError, Response

logger = logging.getLogger(__name__)


class SubscriptionResult(enum.Enum):
    SUBSCRIBED = "subscribed"
    WAITING_CONFIRMATION = "waiting-confirmation"
    UNABLE_TO_SUBSCRIBE = "unable-to-subscribe"


def subscribe(email: str) -> SubscriptionResult:
    if not settings.MAILCHIMP_SECRET_KEY:
        raise ValueError("Mailchimp integration is not configured")

    hashed_email = hashlib.md5(email.encode("utf-8")).hexdigest()
    email_status = get_email_status(hashed_email)

    if email_status == "subscribed":
        # User is already a member, so nothing to do
        return SubscriptionResult.SUBSCRIBED

    status = "subscribed"
    # If the user is unsubscribed or still pending, we ask to confirm again
    if email_status and (email_status == "unsubscribed" or email_status == "pending"):
        status = "pending"

    return subscribe_or_invite_email(email, hashed_email, status)


def subscribe_or_invite_email(
    raw_email: str, hashed_email: str, status: Literal["pending", "subscribed"]
) -> SubscriptionResult:
    response = call_mailchimp_api(
        f"members/{hashed_email}",
        "PUT",
        json={
            "status_if_new": "subscribed",
            "status": status,
            "email_address": raw_email,
        },
    )

    response.raise_for_status()

    if status == "pending":
        return SubscriptionResult.WAITING_CONFIRMATION
    return SubscriptionResult.SUBSCRIBED


def get_email_status(hashed_email: str) -> Optional[str]:
    response = call_mailchimp_api(f"members/{hashed_email}", "GET")

    try:
        response.raise_for_status()
    except HTTPError:
        # If the request fails, assume it is because of a 404
        # or similar. If mailchimp is down we will fail later anyway
        return None

    data = response.json()
    return data["status"]


def call_mailchimp_api(
    endpoint: str,
    method: Literal["GET", "POST", "PUT"],
    *,
    json: Optional[dict[str, any]] = None,
) -> Response:
    base_url = f"https://{settings.MAILCHIMP_DC}.api.mailchimp.com/3.0/lists/{settings.MAILCHIMP_LIST_ID}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {settings.MAILCHIMP_SECRET_KEY}",
    }

    return getattr(requests, method.lower())(
        f"{base_url}/{endpoint}",
        json=json,
        headers=headers,
    )
