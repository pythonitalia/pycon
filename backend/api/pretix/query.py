import math
from decimal import Decimal
from typing import List, Optional

import pretix
import pretix.db
from conferences.models.conference import Conference

from .types import Option, PretixOrder, ProductVariation, Question, TicketItem, Voucher


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


# TODO: we should probably use a category for this
def _is_hotel(item: dict):
    return item.get("default_price") == "0.00"


def _get_category_for_ticket(item, categories):
    category_id = str(item["category"])

    return categories.get(category_id)


def _get_quantity_left_for_ticket(item, quotas):
    if not bool(item["show_quota_left"]):
        return None

    # tickets can be in multiple quotas, in that case the one that has the least amount of tickets
    # should become the source of truth for availability. See:
    # https://docs.pretix.eu/en/latest/development/concepts.html#quotas
    return min(
        quota["available_number"]
        for quota in quotas.values()
        if item["id"] in quota["items"]
    )


def _create_ticket_type_from_api(item, id, categories, questions, quotas, language):
    category = _get_category_for_ticket(item, categories)

    return TicketItem(
        id=id,
        name=item["name"].get("language", item["name"]["en"]),
        description=(
            item["description"].get(language, item["description"]["en"])
            if item["description"]
            else None
        ),
        category=category["name"].get(language, category["name"]["en"]),
        variations=[
            ProductVariation(
                id=variation["id"],
                value=variation["value"].get(language, variation["value"]["en"]),
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
        quantity_left=_get_quantity_left_for_ticket(item, quotas),
    )


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
    categories = pretix.get_categories(conference)
    quotas = pretix.get_quotas(conference)

    def sort_func(ticket):
        # If the item has variations, it means it is the
        # t-shirt product. We want to show it always at the bottom
        if len(ticket.variations) > 0:
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
            if item["active"] and not _is_hotel(item)
        ],
        key=sort_func,
    )
