import math
from decimal import Decimal

from dateutil.parser import parse
from django.utils import timezone

import pretix
from api.pretix.constants import ASSOCIATION_CATEGORY_INTERNAL_NAME
from conferences.models.conference import Conference

from .types import AttendeeTicket, PretixOrder, TicketItem, Voucher


def get_voucher(conference: Conference, code: str) -> Voucher | None:
    return pretix.get_voucher(conference, code)


def get_order(conference: Conference, code: str) -> PretixOrder | None:
    data = pretix.get_order(conference, code)

    if data:
        return PretixOrder.from_data(data)


def get_user_orders(conference, email):
    orders = pretix.get_user_orders(conference, email)

    if orders["count"] == 0:
        return []

    return [PretixOrder.from_data(order) for order in orders["results"]]


def get_user_tickets(
    conference: Conference, email: str, language: str
) -> list[AttendeeTicket]:
    tickets = pretix.get_user_tickets(conference, email)

    if not tickets:
        return []

    categories = pretix.get_categories(conference)
    questions = pretix.get_questions(conference).values()

    return [
        AttendeeTicket.from_data(
            ticket,
            language=language,
            categories=categories,
            questions=questions,
            conference=conference,
        )
        for ticket in tickets
    ]


def _is_ticket_available(item) -> bool:
    now = timezone.now()

    if available_from := item["available_from"]:
        available_from = parse(available_from)

        if available_from >= now:
            return False

    if available_until := item["available_until"]:
        available_until = parse(available_until)

        if available_until < now:
            return False

    return True


def get_conference_tickets(
    conference: Conference, language: str, show_unavailable_tickets: bool = False
) -> list[TicketItem]:
    items = pretix.get_items(conference)

    # hide non active items
    items = {key: item for key, item in items.items() if item["active"]}

    if not show_unavailable_tickets:
        items = {key: item for key, item in items.items() if _is_ticket_available(item)}

    questions = pretix.get_questions(conference).values()
    categories = pretix.get_categories(conference)
    quotas = pretix.get_quotas(conference)

    def sort_func(ticket):
        # Make gadgets and association appear at the end
        if (
            ticket.category == "Gadget"
            or ticket.category_internal_name == ASSOCIATION_CATEGORY_INTERNAL_NAME
        ):
            return math.inf

        # Order all other tickets by price (low -> high)
        return Decimal(ticket.default_price)

    return sorted(
        [
            TicketItem.from_data(
                item,
                categories=categories,
                questions=questions,
                language=language,
                quotas=quotas,
            )
            for item in items.values()
        ],
        key=sort_func,
    )
