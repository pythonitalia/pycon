from typing import List, Optional

import pretix
import pretix.db
from pretix.db import get_user_tickets as pretix_get_user_tickets

from conferences.models.conference import Conference

from .types import (
    Option,
    PretixOrder,
    ProductVariation,
    Question,
    TicketItem,
    UserTicket,
    Voucher,
)


def get_voucher(conference: Conference, code: str) -> Optional[Voucher]:
    return pretix.db.get_voucher(conference.pretix_event_id, code)


def get_user_tickets(
    conference: Conference, user_email: str, language: str
) -> List[UserTicket]:
    tickets = pretix_get_user_tickets(user_email, conference.pretix_event_id)
    return [UserTicket.from_data(ticket, language) for ticket in tickets]


def get_order(conference: Conference, code: str) -> Optional[PretixOrder]:
    data = pretix.get_order(conference, code)

    if data:
        return PretixOrder.from_data(data)


def get_user_orders(conference, email):
    orders = pretix.get_user_orders(conference, email)

    if orders["count"] == 0:
        return []

    return [PretixOrder.from_data(order) for order in orders["results"]]


def get_questions_for_ticket(item, questions, language):
    return [
        Question(
            id=question["id"],
            name=question["question"].get(language, question["question"]["en"]),
            required=question["required"],
            options=[
                Option(
                    id=option["id"],
                    name=option["answer"].get(language, option["answer"]["en"]),
                )
                for option in question["options"]
            ],
        )
        for question in questions
        if item["id"] in question["items"]
    ]


def get_conference_tickets(conference: Conference, language: str) -> List[TicketItem]:
    items = pretix.get_items(conference)
    questions = pretix.get_questions(conference).values()

    # TODO: we should probably use a category for this
    def _is_hotel(item: dict):
        return item.get("default_price") == "0.00"

    return sorted(
        [
            TicketItem(
                id=id,
                name=item["name"].get("language", item["name"]["en"]),
                description=(
                    item["description"].get(language, item["description"]["en"])
                    if item["description"]
                    else None
                ),
                variations=[
                    ProductVariation(
                        id=variation["id"],
                        value=variation["value"].get(
                            language, variation["value"]["en"]
                        ),
                        description=variation["description"].get(language, ""),
                        active=variation["active"],
                        default_price=variation["default_price"],
                    )
                    for variation in item.get("variations", [])
                ],
                active=item["active"],
                default_price=item["default_price"],
                available_from=item["available_from"],
                available_until=item["available_until"],
                questions=get_questions_for_ticket(item, questions, language),
            )
            for id, item in items.items()
            if item["active"] and not _is_hotel(item)
        ],
        key=lambda ticket: len(ticket.variations) > 0,
    )
