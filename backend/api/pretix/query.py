import math
from decimal import Decimal
from typing import List, Optional

from dateutil.parser import parse
from django.utils import timezone

import pretix
import pretix.db
from api.pretix.constants import ASSOCIATION_CATEGORY_INTERNAL_NAME
from conferences.models.conference import Conference

from .types import (
    PretixOrder,
    PretixTicket,
    TicketItem,
    Voucher,
    _create_ticket_type_from_api,
)


def get_voucher(conference: Conference, code: str) -> Optional[Voucher]:
    return pretix.db.get_voucher(conference.pretix_event_id, code)


def get_order(conference: Conference, code: str) -> Optional[PretixOrder]:
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
) -> List[PretixTicket]:
    tickets = pretix.get_user_tickets(conference, email)

    if not tickets:
        return []

    categories = pretix.get_categories(conference)
    return [PretixTicket.from_data(ticket, language, categories) for ticket in tickets]


# TODO: we should probably use a category for this
def _is_hotel(item: dict):
    return item.get("default_price") == "0.00"


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
) -> List[TicketItem]:
    items = pretix.get_items(conference)

    # hide non active items and items that are hotels
    items = {
        key: item
        for key, item in items.items()
        if item["active"] and not _is_hotel(item)
    }

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
            _create_ticket_type_from_api(
                item=item,
                id=id,
                categories=categories,
                questions=questions,
                language=language,
                quotas=quotas,
            )
            for id, item in items.items()
        ],
        key=sort_func,
    )
