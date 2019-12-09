from enum import Enum
from typing import List, Optional

import strawberry

from ..helpers.i18n import make_dict_localized_resolver


@strawberry.enum
class PretixOrderStatus(Enum):
    PENDING = "n"
    PAID = "p"
    EXPIRED = "e"
    CANCELED = "c"


@strawberry.type
class PretixPosition:
    id: int
    name: str = strawberry.field(resolver=make_dict_localized_resolver("name"))
    attendee_name: Optional[str]
    attendee_email: Optional[str]
    price: str

    def __init__(self, position, all_items):
        self.id = position["id"]
        self.attendee_name = position["attendee_name"]
        self.attendee_email = position["attendee_email"]
        self.price = position["price"]

        # TODO: handle item variant?
        self.name = all_items[position["item"]]["name"]


@strawberry.type
class PretixOrder:
    code: str
    status: PretixOrderStatus
    total: str
    url: str
    positions: List[PretixPosition]

    def __init__(self, order, all_items):
        self.code = order["code"]
        self.status = PretixOrderStatus(order["status"])
        self.url = order["url"]
        self.total = order["total"]
        self.positions = [
            PretixPosition(position, all_items) for position in order["positions"]
        ]


@strawberry.type
class TicketItem:
    id: strawberry.ID
    name: str
    description: Optional[str]
    active: bool
    default_price: str
    # TODO: correct types
    available_from: Optional[str]
    available_until: Optional[str]
