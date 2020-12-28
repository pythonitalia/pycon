from datetime import datetime
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
    email: str

    @classmethod
    def from_data(cls, data):
        return cls(
            code=data["code"],
            status=PretixOrderStatus(data["status"]),
            url=data["url"],
            total=data["total"],
            email=data["email"],
        )


@strawberry.type
class ProductVariation:
    id: strawberry.ID
    value: str
    description: str
    active: bool
    default_price: str


@strawberry.type
class Option:
    id: strawberry.ID
    name: str


@strawberry.type
class Question:
    id: strawberry.ID
    name: str
    required: bool
    options: List[Option]


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
    questions: List[Question]


@strawberry.type
class Voucher:
    id: strawberry.ID
    code: str
    valid_until: Optional[datetime]
    value: str
    items: List[strawberry.ID]
    all_items: bool
    redeemed: int
    max_usages: int
    price_mode: str
    variation_id: Optional[strawberry.ID]
