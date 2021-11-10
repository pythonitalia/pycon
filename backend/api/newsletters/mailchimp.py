from dataclasses import dataclass
from django.conf import settings
import requests


@dataclass
class MailchimpSubscription:
    id: str
    email: str


def subscribe(email: str):
    url = f"https://{settings.MAILCHIMP_DC}.api.mailchimp.com/3.0/lists/{settings.MAILCHIMP_LIST_ID}/members"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {settings.MAILCHIMP_DC}",
    }
    response = requests.post(
        url, data={"email_address": email, "status": "subscribed"}, headers=headers
    )

    data = response.json()

    return MailchimpSubscription(id=data["id"], email=data["email"])
