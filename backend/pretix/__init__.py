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


def get_order(conference, code):
    response = pretix(conference, f"orders/{code}/")

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()


def get_user_orders(conference: Conference, email: str):
    response = pretix(conference, "orders", {"email": email})
    response.raise_for_status()
    return response.json()


def get_items(conference: Conference):
    response = pretix(conference, "items")
    response.raise_for_status()

    data = response.json()
    return {result["id"]: result for result in data["results"]}


def get_questions(conference: Conference):
    response = pretix(conference, "questions")
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
    variation: typing.Optional[str]
    attendee_name: str
    attendee_email: str
    answers: typing.Optional[typing.List[CreateOrderTicketAnswer]]


@strawberry.input
class CreateOrderInput:
    email: str
    locale: str
    payment_provider: str
    tickets: typing.List[CreateOrderTicket]


@strawberry.type
class Order:
    code: str
    payment_url: str


def normalize_answers(ticket: CreateOrderTicket, questions: dict):
    answers = []

    for answer in ticket.answers or []:
        question = questions[answer.question_id]

        answer_data = {
            "question": answer.question_id,
            "answer": answer.value,
            "options": [],
            "option_identifier": [],
        }

        print(question)

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


def create_order(conference: Conference, order_data: CreateOrderInput) -> Order:
    questions = get_questions(conference)

    positions = [
        {
            "item": ticket.ticket_id,
            "variation": ticket.variation,
            "attendee_name": ticket.attendee_name,
            "attendee_email": ticket.attendee_email,
            "answers": normalize_answers(ticket, questions),
        }
        for ticket in order_data.tickets
    ]

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

        raise PretixError(response.content.decode("utf-8"))

    response.raise_for_status()

    data = response.json()

    return Order(code=data["code"], payment_url=data["payments"][0]["payment_url"])
