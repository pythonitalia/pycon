from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

import strawberry

from api.pretix.constants import ASSOCIATION_CATEGORY_INTERNAL_NAME
from pretix.types import Quota


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

    @classmethod
    def from_data(cls, data, language: str):
        return cls(
            id=data["id"],
            name=_get_by_language(data, "answer", language),
        )


@strawberry.type
class Question:
    id: strawberry.ID
    name: str
    required: bool
    options: List[Option]

    @classmethod
    def from_data(cls, data, language: str):
        return cls(
            id=data["id"],
            name=_get_by_language(data, "question", language),
            required=data["required"],
            options=[Option.from_data(option, language) for option in data["options"]],
        )


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
    def from_data(
        cls,
        data,
        language: str,
        categories,
        questions,
        quotas: Optional[Dict[str, Quota]] = None,
    ):
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
            questions=[
                Question.from_data(question, language)
                for question in questions
                if data["id"] in question["items"]
            ],
            quantity_left=cls._get_quantity_left(data, quotas),
        )

    @staticmethod
    def _get_quantity_left(data, quotas: Optional[Dict[str, Quota]]):
        if not bool(data["show_quota_left"]):
            return None

        # For user's tickets we don't need quantity left
        if not quotas:
            return None

        # tickets can be in multiple quotas, in that case the one that has the least amount of tickets
        # should become the source of truth for availability. See:
        # https://docs.pretix.eu/en/latest/development/concepts.html#quotas
        return min(
            quota["available_number"]
            for quota in quotas.values()
            if int(data["id"]) in quota["items"]
        )


@strawberry.type
class PretixOrderPosition:
    id: strawberry.ID
    name: str
    email: str
    item: TicketItem

    @classmethod
    def from_data(cls, data, language: str, categories):
        item = data["item"]
        questions = [answer["question"] for answer in data["answers"]]
        return cls(
            id=data["id"],
            name=data["attendee_name"],
            email=data["attendee_email"],
            item=TicketItem.from_data(item, language, categories, questions),
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
