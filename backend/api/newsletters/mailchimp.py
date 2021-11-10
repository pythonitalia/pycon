from dataclasses import dataclass
from django.conf import settings
import requests


@dataclass
class MailchimpSubscription:
    id: str
    email: str


def subscribe(email: str):
    url = f"https://${settings.MAILCHIMP_DC}.api.mailchimp.com/3.0/lists/{settings.MAILCHIMP_LIST_ID}/members"

    response = requests.post(url, json={"email_address": email, "status": "subscribed"})

    data = response.json()
    return MailchimpSubscription(id=data["id"], email=data["email"])
