import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class MailchimpError(Exception):
    def __init__(self, title, detail="", status=""):
        message = f"{status} {title}: {detail}"

        return super().__init__(message)


def subscribe(email: str) -> bool:
    if not settings.MAILCHIMP_SECRET_KEY:
        raise ValueError("Mailchimp integration is not configured")

    url = f"https://{settings.MAILCHIMP_DC}.api.mailchimp.com/3.0/lists/{settings.MAILCHIMP_LIST_ID}/members"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {settings.MAILCHIMP_SECRET_KEY}",
    }

    response = requests.post(
        url, json={"email_address": email, "status": "subscribed"}, headers=headers
    )

    data = response.json()
    if data["status"] == "subscribed" or data["title"] == "Member Exists":
        return True
    else:
        logger.error("Error from mailchimp: %s", data)
        raise MailchimpError(
            status=data.get("status"),
            title=data.get("title"),
            detail=data.get("detail"),
        )
