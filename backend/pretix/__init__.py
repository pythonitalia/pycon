from urllib.parse import urljoin

import requests
from django.conf import settings


def get_api_url(conference, endpoint, query):
    return urljoin(
        settings.PRETIX_API,
        f"organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/{endpoint}",  # noqa
    ) + append_qs(query)


def append_qs(querystring):
    items = querystring.items()

    if len(items) > 0:
        return "?" + "&".join([f"{key}={value}" for key, value in items])

    return ""


def pretix(conference, endpoint, qs={}):
    return requests.get(
        get_api_url(conference, endpoint, qs),
        headers={"Authorization": f"Token {settings.PRETIX_API_TOKEN}"},
    )


def get_user_orders(conference, email):
    response = pretix(conference, "orders", {"email": email})
    response.raise_for_status()
    return response.json()


def get_items(conference):
    response = pretix(conference, "items")
    response.raise_for_status()

    data = response.json()
    return {result["id"]: result for result in data["results"]}
