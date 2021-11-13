from dataclasses import dataclass

import requests
from django.conf import settings


@dataclass
class MailchimpSubscription:
    id: str
    email: str


def subscribe(email: str):
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

    return MailchimpSubscription(id=data["id"], email=data["email_address"])
