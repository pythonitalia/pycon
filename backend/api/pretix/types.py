from datetime import datetime
from enum import Enum
from typing import List, Optional

import strawberry

from api.pretix.constants import ASSOCIATION_CATEGORY_INTERNAL_NAME


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

    @classmethod
    def from_data(cls, data, language: str):
        return cls(
            id=data["id"],
            value=_get_by_language(data, "value", language),
            description=_get_by_language(data, "description", language),
            active=data["active"],
            default_price=data["default_price"],
        )


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


@strawberry.enum
class TicketType(Enum):
    STANDARD = "standard"
    BUSINESS = "business"
    ASSOCIATION = "association"


def _get_category_for_ticket(item, categories):
    category_id = str(item["category"])

    return categories.get(category_id)


def _get_by_language(item, key, language):
    return item[key].get(language, item[key]["en"]) if item[key] else None


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


def _create_ticket_type_from_api(item, id, categories, questions, quotas, language):
    category = _get_category_for_ticket(item, categories)

    return TicketItem(
        id=id,
        language=language,
        name=_get_by_language(item, "name", language),
        description=_get_by_language(item, "description", language),
        category=_get_by_language(category, "name", language),
        category_internal_name=category.get("internal_name", None),
        variations=[
            ProductVariation(
                id=variation["id"],
                value=_get_by_language(variation, "value", language),
                description=_get_by_language(variation, "description", language),
                active=variation["active"],
                default_price=variation["default_price"],
            )
            for variation in item.get("variations", [])
        ],
        tax_rate=item["tax_rate"],
        active=item["active"],
        default_price=item["default_price"],
        available_from=item["available_from"],
        available_until=item["available_until"],
        questions=get_questions_for_ticket(item, questions, language),
        quantity_left=_get_quantity_left_for_ticket(item, quotas),
    )


@strawberry.type
class TicketItem:
    id: strawberry.ID
    name: str
    language: str
    description: Optional[str]
    active: bool
    default_price: str
    category: str
    category_internal_name: Optional[str]
    tax_rate: float
    variations: List[ProductVariation]
    # TODO: correct types
    available_from: Optional[str]
    available_until: Optional[str]
    questions: List[Question]
    quantity_left: Optional[int]

    @strawberry.field
    def type(self) -> TicketType:
        if "business" in self.name.lower():
            return TicketType.BUSINESS

        if self.category_internal_name == ASSOCIATION_CATEGORY_INTERNAL_NAME:
            return TicketType.ASSOCIATION

        return TicketType.STANDARD

    @classmethod
    def from_data(cls, data, language: str, categories):
        category = _get_category_for_ticket(data, categories)

        return cls(
            id=data["id"],
            language=language,
            name=_get_by_language(data, "name", language),
            description=_get_by_language(data, "description", language),
            tax_rate=data["tax_rate"],
            active=data["active"],
            default_price=data["default_price"],
            available_from=data["available_from"],
            available_until=data["available_until"],
            category=_get_by_language(category, "name", language),
            category_internal_name=category.get("internal_name", None),
            variations=[
                ProductVariation.from_data(variation, language)
                for variation in data.get("variations", [])
            ],
            questions=[],
            quantity_left=None,
        )


@strawberry.type
class PretixTicket:
    price: str
    item: TicketItem

    @classmethod
    def from_data(cls, data, language: str, categories):
        item = data["item"]
        return cls(
            price=data["price"], item=TicketItem.from_data(item, language, categories)
        )


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
