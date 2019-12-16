import itertools
import logging
import typing
from urllib.parse import urljoin

import requests
import strawberry
from conferences.models.conference import Conference
from django.conf import settings

from .exceptions import PretixError

logger = logging.getLogger(__file__)


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


def pretix(conference, endpoint, qs={}, method="get", **kwargs):
    method = getattr(requests, method)

    return method(
        get_api_url(conference, endpoint, qs),
        headers={"Authorization": f"Token {settings.PRETIX_API_TOKEN}"},
        **kwargs,
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


@strawberry.input
class CreateOrderTicket:
    ticket_id: str
    variation: typing.Optional[str]
    quantity: int


@strawberry.input
class CreateOrderInput:
    email: str
    locale: str
    payment_provider: str
    tickets: typing.List[CreateOrderTicket]


@strawberry.type
class Order:
    payment_url: str


def create_order(conference: Conference, order_data: CreateOrderInput) -> Order:
    positions = list(
        itertools.chain(
            *[
                [{"item": ticket.ticket_id, "variation": ticket.variation}]
                * ticket.quantity
                for ticket in order_data.tickets
            ]
        )
    )

    payload = {
        "email": order_data.email,
        "locale": order_data.locale,
        "payment_provider": order_data.payment_provider,
        "testmode": True,
        "positions": positions,
    }

    # it needs the / at the end...
    response = pretix(conference, "orders/", method="post", json=payload)

    if response.status_code == 400:
        logger.warning("Unable to create order on pretix %s", response.content)

        errors = [" ".join(errors) for key, errors in response.json().items()]
        message = " ".join(errors)

        raise PretixError(message)

    response.raise_for_status()

    data = response.json()

    return Order(payment_url=data["payments"][0]["payment_url"])
