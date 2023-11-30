import logging
from datetime import date
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin
from django.utils.dateparse import parse_datetime
import requests
import strawberry
from django.conf import settings
from django.core.cache import cache
from api.pretix.types import UpdateAttendeeTicketInput, Voucher
from conferences.models.conference import Conference
from hotels.models import BedLayout, HotelRoom
from pretix.types import Category, Question, Quota
import sentry_sdk

from .exceptions import PretixError

logger = logging.getLogger(__file__)


def get_api_url(conference: Conference, endpoint: str) -> str:
    return urljoin(
        settings.PRETIX_API,
        f"organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/{endpoint}",  # noqa
    )


def _pretix_request(
    conference: Conference,
    url: str,
    qs: Optional[Dict[str, Any]] = None,
    method="get",
    **kwargs,
):
    return requests.request(
        method,
        url,
        params=qs or {},
        headers={"Authorization": f"Token {settings.PRETIX_API_TOKEN}"},
        **kwargs,
    )


def pretix(
    conference: Conference,
    endpoint: str,
    qs: Optional[Dict[str, Any]] = None,
    method="get",
    **kwargs,
):
    url = get_api_url(conference, endpoint)

    return _pretix_request(conference, url, qs, method, **kwargs)


def get_voucher(conference: Conference, code: str) -> Optional[Voucher]:
    response = pretix(conference, f"extended-vouchers/{code}/")

    if response.status_code == 404:
        return None

    response.raise_for_status()
    data = response.json()

    items = []
    all_items = False

    if data["item"]:
        # Only the selected item is included in the voucher
        items = [data["item"]]
    elif data["quota"]:
        # If a quota is specified only items in that quota are valid
        items = data["quota_items"]
    else:
        # No item or quota found
        # it means that this voucher code covers all items
        all_items = True

    return Voucher(
        id=data["id"],
        code=data["code"],
        valid_until=parse_datetime(data["valid_until"])
        if data["valid_until"]
        else None,
        value=data["value"],
        items=items,
        all_items=all_items,
        redeemed=data["redeemed"],
        max_usages=data["max_usages"],
        price_mode=data["price_mode"],
        variation_id=data["variation"],
    )


def create_voucher(
    conference: Conference,
    code: str,
    comment: str,
    tag: str,
    quota_id: int,
    price_mode: str,
    value: str,
):
    payload = {
        "code": code,
        "comment": comment,
        "tag": tag,
        "max_usages": 1,
        "valid_until": None,
        "block_quota": False,
        "allow_ignore_quota": False,
        "price_mode": price_mode,
        "value": value,
        "item": None,
        "variation": None,
        "quota": quota_id,
        "subevent": None,
    }
    response = pretix(conference, "vouchers/", method="post", json=payload)
    response.raise_for_status()
    return response.json()


def get_order(conference: Conference, code: str):
    response = pretix(conference, f"orders/{code}/")

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()


def get_user_orders(conference: Conference, email: str):
    response = pretix(conference, "orders", {"email": email})
    response.raise_for_status()
    return response.json()


def _get_paginated(
    conference: Conference, endpoint: str, qs: Optional[Dict[str, Any]] = None
):
    url = get_api_url(conference, endpoint)

    while url is not None:
        response = requests.get(
            url,
            params=qs,
            headers={"Authorization": f"Token {settings.PRETIX_API_TOKEN}"},
        )

        response.raise_for_status()

        data = response.json()
        url = data.get("next")

        yield from (order for order in data["results"])


def get_orders(conference: Conference):
    return _get_paginated(conference, "orders")


def get_all_order_positions(
    conference: Conference, params: Optional[Dict[str, Any]] = None
):
    return _get_paginated(conference, "orderpositions", params)


def get_invoices(conference: Conference):
    return _get_paginated(conference, "invoices")


def get_items(conference: Conference, params: Optional[Dict[str, Any]] = None):
    response = pretix(conference, "items", params)
    response.raise_for_status()

    data = response.json()
    return {str(result["id"]): result for result in data["results"]}


def cache_pretix(name: str):
    def factory(func):
        def wrapper(*args, **kwargs):
            conference = args[0]
            cache_key = (
                f"pretix:"
                f"{conference.pretix_organizer_id}:{conference.pretix_event_id}:"
                f"{name}"
            )

            if cache.has_key(cache_key):
                return cache.get(cache_key)

            value = func(*args, **kwargs)
            cache.set(cache_key, value, timeout=60 * 60 * 24 * 7)
            return value

        return wrapper

    return factory


@cache_pretix(name="questions")
def get_questions(conference: Conference) -> Dict[str, Question]:
    response = pretix(conference, "questions")
    response.raise_for_status()

    data = response.json()
    return {str(result["id"]): result for result in data["results"]}


@cache_pretix(name="categories")
def get_categories(conference: Conference) -> Dict[str, Category]:
    response = pretix(conference, "categories")
    response.raise_for_status()
    data = response.json()
    return {str(result["id"]): result for result in data["results"]}


def get_quotas(conference: Conference) -> Dict[str, Quota]:
    response = pretix(conference, "quotas", qs={"with_availability": "true"})
    response.raise_for_status()

    data = response.json()
    return {str(result["id"]): result for result in data["results"]}


@strawberry.input
class CreateOrderTicketAnswer:
    question_id: str
    value: str


@strawberry.input
class CreateOrderTicket:
    ticket_id: str
    attendee_name: str
    attendee_email: str
    variation: Optional[str] = None
    answers: Optional[List[CreateOrderTicketAnswer]] = None
    voucher: Optional[str] = None


@strawberry.input
class CreateOrderHotelRoom:
    room_id: str
    bed_layout_id: str
    checkin: date
    checkout: date


@strawberry.input
class InvoiceInformation:
    is_business: bool
    company: Optional[str]
    name: str
    street: str
    zipcode: str
    city: str
    country: str
    vat_id: str
    fiscal_code: str
    pec: str | None = None
    sdi: str | None = None


@strawberry.input
class CreateOrderInput:
    email: str
    locale: str
    payment_provider: str
    invoice_information: InvoiceInformation
    tickets: List[CreateOrderTicket]
    hotel_rooms: List[CreateOrderHotelRoom]


@strawberry.type
class Order:
    code: str
    payment_url: str


def normalize_answers(ticket: CreateOrderTicket, questions: dict):
    answers = []

    for answer in ticket.answers or []:
        question = questions[answer.question_id]

        if not answer.value and not question.get("required", False):
            continue

        answer_data = {
            "question": answer.question_id,
            "answer": answer.value,
            "options": [],
            "option_identifier": [],
        }

        # TODO: support more question types
        if question["type"] == "C":
            option = next(
                (
                    option
                    for option in question["options"]
                    if str(option["id"]) == answer.value
                ),
                None,
            )

            if option:
                answer_data["options"] = [option["id"]]
                answer_data["option_identifiers"] = [option["identifier"]]
            else:
                raise ValueError("Unable to find option")

        answers.append(answer_data)

    return answers


def normalize_position(ticket: CreateOrderTicket, items: dict, questions: dict):
    item = items[ticket.ticket_id]

    data = {
        "item": ticket.ticket_id,
        "variation": ticket.variation,
        "answers": normalize_answers(ticket, questions),
    }

    if ticket.voucher:
        data["voucher"] = ticket.voucher

    if item["admission"]:
        data["attendee_name"] = ticket.attendee_name
        data["attendee_email"] = ticket.attendee_email

    return data


def create_hotel_positions(
    hotel_rooms: List[CreateOrderHotelRoom], locale: str, conference: Conference
):
    rooms: List[HotelRoom] = list(HotelRoom.objects.filter(conference=conference).all())
    bed_layouts: List[BedLayout] = list(BedLayout.objects.all())

    positions = []

    for order_room in hotel_rooms:
        room = [room for room in rooms if str(room.pk) == order_room.room_id][0]
        bed_layout = next(
            layout
            for layout in bed_layouts
            if str(layout.id) == order_room.bed_layout_id
        )

        num_nights = (order_room.checkout - order_room.checkin).days
        total_price = num_nights * room.price

        positions.append(
            {
                "item": conference.pretix_hotel_ticket_id,
                "price": str(total_price),
                "answers": [
                    {
                        "question": conference.pretix_hotel_room_type_question_id,
                        "answer": room.name.localize(locale),
                        "options": [],
                        "option_identifier": [],
                    },
                    {
                        "question": conference.pretix_hotel_checkin_question_id,
                        "answer": order_room.checkin.strftime("%Y-%m-%d"),
                        "options": [],
                        "option_identifier": [],
                    },
                    {
                        "question": conference.pretix_hotel_checkout_question_id,
                        "answer": order_room.checkout.strftime("%Y-%m-%d"),
                        "options": [],
                        "option_identifier": [],
                    },
                    {
                        "question": conference.pretix_hotel_bed_layout_question_id,
                        "answer": bed_layout.name.localize(locale),
                        "options": [],
                        "option_identifier": [],
                    },
                ],
            }
        )

    return positions


def create_order(conference: Conference, order_data: CreateOrderInput) -> Order:
    questions = get_questions(conference)
    items = get_items(conference)

    positions = [
        normalize_position(ticket, items, questions) for ticket in order_data.tickets
    ]

    if len(order_data.hotel_rooms) > 0:
        positions.extend(
            create_hotel_positions(
                order_data.hotel_rooms, order_data.locale, conference
            )
        )

    payload = {
        "email": order_data.email,
        "locale": order_data.locale,
        "payment_provider": order_data.payment_provider,
        "testmode": False,
        "positions": positions,
        "invoice_address": {
            "is_business": order_data.invoice_information.is_business,
            "company": order_data.invoice_information.company,
            "name_parts": {"full_name": order_data.invoice_information.name},
            "street": order_data.invoice_information.street,
            "zipcode": order_data.invoice_information.zipcode,
            "city": order_data.invoice_information.city,
            "country": order_data.invoice_information.country,
            "vat_id": order_data.invoice_information.vat_id,
            "internal_reference": order_data.invoice_information.fiscal_code,
        },
    }

    # it needs the / at the end...
    response = pretix(conference, "orders/", method="post", json=payload)

    if response.status_code == 400:
        logger.warning("Unable to create order on pretix %s", response.content)

        raise PretixError(response.content.decode("utf-8"))

    response.raise_for_status()

    data = response.json()

    if order_data.invoice_information.country == "IT":
        response = _pretix_request(
            conference,
            urljoin(
                settings.PRETIX_API,
                f"orders/{data['code']}/update_invoice_information/",
            ),
            method="post",
            json={
                "pec": order_data.invoice_information.pec,
                "codice_fiscale": order_data.invoice_information.fiscal_code,
                "sdi": order_data.invoice_information.sdi,
            },
        )

        if response.status_code != 200:
            with sentry_sdk.push_scope() as scope:
                scope.user = {"email": order_data.email}
                scope.set_extra("order-code", data["code"])
                scope.set_extra("pec", order_data.invoice_information.pec)
                scope.set_extra(
                    "codice_fiscale", order_data.invoice_information.fiscal_code
                )
                scope.set_extra("sdi", order_data.invoice_information.sdi)

                sentry_sdk.capture_message(
                    f"Unable to update invoice information for order {data['code']}",
                    level="error",
                )

    return Order(code=data["code"], payment_url=data["payments"][0]["payment_url"])


def user_has_admission_ticket(
    *,
    email: str,
    event_organizer: str,
    event_slug: str,
    additional_events: Optional[List[dict]] = None,
) -> bool:
    additional_events = additional_events or []
    events = [
        {
            "organizer_slug": event_organizer,
            "event_slug": event_slug,
        }
    ] + additional_events
    response = pretix(
        conference=Conference(
            pretix_organizer_id=event_organizer, pretix_event_id=event_slug
        ),
        endpoint="tickets/attendee-has-ticket/",
        method="post",
        json={
            "attendee_email": email,
            "events": events,
        },
    )

    response.raise_for_status()

    data = response.json()
    return data["user_has_admission_ticket"]


def get_user_tickets(conference: Conference, email: str):
    response = pretix(
        conference=conference,
        endpoint="tickets/attendee-tickets",
        method="get",
        qs={
            "attendee_email": email,
        },
    )

    response.raise_for_status()

    return response.json()


@cache_pretix(name="all_vouchers")
def get_all_vouchers(conference: Conference):
    vouchers = _get_paginated(conference, "vouchers")
    vouchers_by_id = {voucher["id"]: voucher for voucher in vouchers}
    return vouchers_by_id


def get_user_ticket(conference: Conference, email: str, id: str):
    # TODO: filter by orderposition in the PretixAPI
    tickets = get_user_tickets(conference, email)

    def filter_by(ticket):
        return (
            str(ticket["id"]) == str(id)
            and ticket["attendee_email"].lower() == email.lower()
        )

    tickets = list(filter(filter_by, tickets))

    if tickets:
        return tickets[0]


def is_ticket_owner(conference: Conference, email: str, id: str) -> bool:
    ticket = get_user_ticket(conference, email, id)
    return ticket is not None


def update_ticket(conference: Conference, attendee_ticket: UpdateAttendeeTicketInput):
    response = pretix(
        conference=conference,
        endpoint=f"orderpositions/{attendee_ticket.id}/",
        method="PATCH",
        json=attendee_ticket.to_json(),
    )

    response.raise_for_status()

    return response.json()


def get_order_position(conference: Conference, id: str):
    response = pretix(
        conference=conference,
        endpoint=f"orderpositions/{id}/",
        method="GET",
    )

    response.raise_for_status()

    return response.json()
