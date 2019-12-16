from enum import Enum
from typing import List, Optional

import strawberry


@strawberry.enum
class PretixOrderStatus(Enum):
    PENDING = "n"
    PAID = "p"
    EXPIRED = "e"
    CANCELED = "c"


@strawberry.type
class PretixOrder:
    code: str
    status: PretixOrderStatus
    total: str
    url: str

    def __init__(self, order):
        self.code = order["code"]
        self.status = PretixOrderStatus(order["status"])
        self.url = order["url"]
        self.total = order["total"]


@strawberry.type
class ProductVariation:
    id: strawberry.ID
    value: str
    description: str
    active: bool
    default_price: str


@strawberry.type
class TicketItem:
    id: strawberry.ID
    name: str
    description: Optional[str]
    active: bool
    default_price: str
    variations: List[ProductVariation]
    # TODO: correct types
    available_from: Optional[str]
    available_until: Optional[str]
