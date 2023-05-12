from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import strawberry

from api.pretix.constants import (
    ASSOCIATION_CATEGORY_INTERNAL_NAME,
    SOCIAL_EVENTS_CATEGORY_INTERNAL_NAME,
)
from pretix.types import (
    Answer as AnswerDict,
    Category as CategoryDict,
    Item as ItemDict,
    Option as OptionDict,
    OrderPosition as OrderPositionDict,
    ProductVariation as ProductVariationDict,
    Question as QuestionDict,
    Quota as QuotaDict,
)
from api.context import Info
from conferences.models.conference import Conference
from badges.roles import ConferenceRole, get_conference_roles_for_ticket_data


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
    def from_data(cls, data) -> PretixOrder:
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
    quantity_left: Optional[int]
    sold_out: Optional[bool]

    @classmethod
    def from_data(
        cls,
        data: ProductVariationDict,
        language: str,
        quotas: Optional[Dict[str, QuotaDict]],
        parent_item_id: int,
    ) -> ProductVariation:
        quantity_left = TicketItem._get_quantity_left(
            data, quotas, parent_item_id=parent_item_id
        )
        sold_out = quantity_left <= 0 if quantity_left is not None else False

        return cls(
            id=data["id"],
            value=_get_by_language(data, "value", language),
            description=_get_by_language(data, "description", language),
            active=data["active"],
            default_price=data["default_price"],
            sold_out=sold_out,
            quantity_left=None,
        )


@strawberry.type
class Option:
    id: strawberry.ID
    name: str

    @classmethod
    def from_data(cls, data: OptionDict, language: str) -> Option:
        return cls(
            id=data["id"],
            name=_get_by_language(data, "answer", language),
        )


@strawberry.type
class Answer:
    answer: str
    options: Optional[List[str]]

    @classmethod
    def from_data(cls, data: QuestionDict, language: str) -> Answer:
        # If it's an option answer it's not translated
        if data.get("options"):
            options = [
                option
                for option in data["options"]
                if option["id"] in data["answer"]["options"]
            ]
            options_answers = [
                _get_by_language(option, "answer", language) for option in options
            ]
            return cls(
                answer=", ".join(options_answers), options=data["answer"]["options"]
            )

        return cls(answer=data["answer"]["answer"], options=[])


@strawberry.type
class Question:
    id: strawberry.ID
    name: str
    required: Optional[bool]
    hidden: bool
    options: Optional[List[Option]]
    answer: Optional[Answer]

    @classmethod
    def from_data(cls, data: QuestionDict, language: str) -> Question:
        return cls(
            id=data["id"],
            name=_get_by_language(data, "question", language),
            required=data["required"],
            hidden=data["hidden"],
            options=[Option.from_data(option, language) for option in data["options"]],
            answer=Answer.from_data(data, language) if data.get("answer") else None,
        )


@strawberry.enum
class TicketType(Enum):
    STANDARD = "standard"
    BUSINESS = "business"
    ASSOCIATION = "association"
    HOTEL = "hotel"
    SOCIAL_EVENT = "social-event"


def _get_category_for_ticket(item, categories):
    category_id = str(item["category"])

    return categories.get(category_id)


def _get_by_language(item, key, language):
    return item[key].get(language, item[key]["en"]) if item[key] else None


@strawberry.type
class TicketItem:
    id: strawberry.ID
    name: str
    admission: bool
    language: Optional[str]
    description: Optional[str]
    active: Optional[bool]
    default_price: Optional[str]
    category: Optional[str]
    category_internal_name: Optional[str]
    tax_rate: Optional[float]
    variations: Optional[List[ProductVariation]]
    # TODO: correct types
    available_from: Optional[str]
    available_until: Optional[str]
    questions: Optional[List[Question]]
    quantity_left: Optional[int]
    sold_out: Optional[bool]

    @strawberry.field
    def type(self) -> Optional[TicketType]:
        if "business" in self.name.lower():
            return TicketType.BUSINESS

        if self.category_internal_name == ASSOCIATION_CATEGORY_INTERNAL_NAME:
            return TicketType.ASSOCIATION

        if self.category_internal_name == SOCIAL_EVENTS_CATEGORY_INTERNAL_NAME:
            return TicketType.SOCIAL_EVENT

        return TicketType.STANDARD

    @classmethod
    def from_data(
        cls,
        data: ItemDict,
        language: str,
        categories: Dict[str, CategoryDict],
        questions: Dict[str, Question],
        quotas: Optional[Dict[str, QuotaDict]] = None,
    ):
        category = _get_category_for_ticket(data, categories)
        show_quantity_left = data.get("show_quota_left", False)

        if data["has_variations"]:
            # if the product has variations
            # each variation has it is own quantity and sold out state
            # so the parent product doesn't matter
            quantity_left = None
            sold_out = False
        else:
            quantity_left = cls._get_quantity_left(data, quotas)
            sold_out = quantity_left <= 0 if quantity_left is not None else False

        return cls(
            id=data["id"],
            language=language,
            name=_get_by_language(data, "name", language),
            description=_get_by_language(data, "description", language),
            tax_rate=data["tax_rate"],
            active=data["active"],
            admission=data["admission"],
            default_price=data["default_price"],
            available_from=data["available_from"],
            available_until=data["available_until"],
            category=_get_by_language(category, "name", language),
            category_internal_name=category.get("internal_name", None),
            variations=[
                ProductVariation.from_data(
                    variation, language, quotas, parent_item_id=data["id"]
                )
                for variation in data.get("variations", [])
            ],
            questions=[
                Question.from_data(question, language)
                for question in questions
                if data["id"] in question["items"]
            ],
            sold_out=sold_out,
            quantity_left=quantity_left if show_quantity_left else None,
        )

    @staticmethod
    def _get_quantity_left(
        data,
        quotas: Optional[Dict[str, QuotaDict]],
        parent_item_id: Optional[int] = None,
    ):
        # For user's tickets we don't need quantity left
        if not quotas:
            return None

        # tickets can be in multiple quotas, in that case the one
        # that has the least amount of tickets
        # should become the source of truth for availability. See:
        # https://docs.pretix.eu/en/latest/development/concepts.html#quotas
        if parent_item_id:
            return min(
                quota["available_number"]
                for quota in quotas.values()
                if int(parent_item_id) in quota["items"]
                and int(data["id"]) in quota["variations"]
            )
        else:
            return min(
                quota["available_number"]
                for quota in quotas.values()
                if int(data["id"]) in quota["items"]
            )


def get_questions_with_answers(questions: List[QuestionDict], data: OrderPositionDict):
    def get_answer(question_id: int) -> Optional[AnswerDict]:
        return next(
            filter(lambda a: a["question"]["id"] == question_id, data["answers"]),
            None,
        )

    questions_with_answers = []
    for question in questions:
        if data["item"]["id"] not in question["items"]:
            continue
        answer = get_answer(question["id"])
        question["answer"] = answer

        questions_with_answers.append(question)

    return questions_with_answers


@strawberry.type
class AttendeeTicket:
    id: strawberry.ID
    name: Optional[str]
    email: Optional[str]
    secret: str
    variation: Optional[strawberry.ID]
    item: TicketItem
    _conference: strawberry.Private[Conference]
    _data: strawberry.Private[Any]

    @strawberry.field
    def role(self, info: Info) -> ConferenceRole | None:
        if not self.item.admission:
            return None

        return get_conference_roles_for_ticket_data(
            conference=self._conference,
            user_id=info.context.request.user.id,
            data=self._data,
        )[0]

    @classmethod
    def from_data(
        cls,
        data: OrderPositionDict,
        language: str,
        categories: Dict[str, CategoryDict],
        questions: List[QuestionDict],
        conference: Conference,
    ):
        data["item"]["questions"] = get_questions_with_answers(
            questions,
            data,
        )

        return cls(
            id=data["id"],
            name=data["attendee_name"],
            email=data["attendee_email"],
            secret=data["secret"],
            variation=data["variation"],
            item=TicketItem.from_data(
                data["item"],
                language=language,
                categories=categories,
                questions=data["item"]["questions"],
            ),
            _conference=conference,
            _data=data,
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


@strawberry.input
class AnswerInput:
    answer: str
    question: strawberry.ID
    options: Optional[List[strawberry.ID]] = None

    def to_json(self):
        data = {"answer": self.answer, "question": self.question}
        if self.options:
            data["options"] = self.options

        return data


@strawberry.input
class UpdateAttendeeTicketInput:
    id: strawberry.ID
    name: str
    email: str
    answers: Optional[List[AnswerInput]] = None

    def to_json(self):
        return {
            "attendee_email": self.email,
            "attendee_name": self.name,
            "answers": [answer.to_json() for answer in self.answers]
            if self.answers
            else [],
        }
