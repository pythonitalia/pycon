from datetime import datetime
from enum import Enum
from typing import List, Optional

from api.helpers.ids import encode_hashid

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


@strawberry.type
class UserTicketAnswer:
    id: strawberry.ID
    question_id: strawberry.ID
    answer: Optional[str]

    @classmethod
    def from_data(cls, data, language):
        return cls(
            id=encode_hashid(data["id"]),
            question_id=data["question_id"],
            answer=data["answer"],
        )


@strawberry.type
class UserTicket:
    id: strawberry.ID
    item_id: strawberry.ID
    ticket_name: str
    attendee_name: str
    attendee_email: str
    answers: List[UserTicketAnswer]

    @classmethod
    def from_data(cls, data, language):
        return cls(
            id=encode_hashid(data["position_id"]),
            item_id=data["item_id"],
            ticket_name=data["item_name"].get(language, data["item_name"]["en"]),
            attendee_name=data["attendee_name"],
            attendee_email=data["attendee_email"],
            answers=[
                UserTicketAnswer.from_data(answer, language)
                for answer in data["answers"]
            ],
        )
