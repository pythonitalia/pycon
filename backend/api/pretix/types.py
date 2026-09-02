from api.types import BaseErrorType
from api.utils import validate_email
from strawberry.scalars import JSON

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Self

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
from api.helpers.ids import encode_hashid
from countries import countries
from billing.validation import (
    validate_italian_zip_code,
    validate_fiscal_code,
    validate_italian_vat_number,
    validate_sdi_code,
)
from billing.exceptions import (
    ItalianZipCodeValidationError,
    FiscalCodeValidationError,
    ItalianVatNumberValidationError,
    SdiValidationError,
)


@strawberry.type
class AnswerInputError:
    answer: list[str] = strawberry.field(default_factory=list)
    question: list[str] = strawberry.field(default_factory=list)
    options: list[str] = strawberry.field(default_factory=list)
    non_field_errors: list[str] = strawberry.field(default_factory=list)


@strawberry.type
class AttendeeNameInputError:
    given_name: list[str] = strawberry.field(default_factory=list)
    family_name: list[str] = strawberry.field(default_factory=list)
    non_field_errors: list[str] = strawberry.field(default_factory=list)


@strawberry.type
class UpdateAttendeeTicketErrors(BaseErrorType):
    @strawberry.type
    class _UpdateAttendeeTicketErrors:
        id: list[str] = strawberry.field(default_factory=list)
        attendee_name: AttendeeNameInputError = strawberry.field(
            default_factory=AttendeeNameInputError
        )
        attendee_email: list[str] = strawberry.field(default_factory=list)
        answers: list[AnswerInputError] = strawberry.field(default_factory=list)

    errors: _UpdateAttendeeTicketErrors = None


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
    def from_data(cls, data) -> Self:
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
    ) -> Self:
        quantity_left = TicketItem._get_quantity_left(
            data, quotas, parent_item_id=parent_item_id
        )
        sold_out = quantity_left <= 0 if quantity_left is not None else False

        return cls(
            id=data["id"],
            value=_get_by_language(data, "value", language),
            description=_get_by_language(data, "description", language) or "",
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
    def from_data(cls, data: OptionDict, language: str) -> Self:
        return cls(
            id=data["id"],
            name=_get_by_language(data, "answer", language),
        )


@strawberry.type
class Answer:
    answer: str
    options: Optional[List[str]]

    @classmethod
    def from_data(cls, data: QuestionDict, language: str) -> Self:
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
    def from_data(cls, data: QuestionDict, language: str) -> Self:
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
class AttendeeName:
    parts: JSON
    scheme: str

    @classmethod
    def from_pretix_api(cls, data):
        scheme = data.pop("_scheme", data.pop("scheme", "legacy"))
        return cls(
            parts=data,
            scheme=scheme,
        )


@strawberry.input
class AttendeeNameInput:
    parts: JSON
    scheme: str

    def to_pretix_api(self):
        return self.parts

    def validate(self, errors: BaseErrorType):
        if not self.parts:
            errors.add_error("non_field_errors", "This field may not be blank.")
            return False

        if self.scheme == "given_family":
            given_name = self.parts.get("given_name", "").strip()
            family_name = self.parts.get("family_name", "").strip()

            if not given_name:
                errors.add_error("given_name", "This field may not be blank.")

            if not family_name:
                errors.add_error("family_name", "This field may not be blank.")

        return errors


@strawberry.type
class AttendeeTicket:
    id: strawberry.ID
    hashid: strawberry.ID
    attendee_name: Optional[AttendeeName]
    attendee_email: Optional[str]
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
            hashid=encode_hashid(data["id"]),
            attendee_name=AttendeeName.from_pretix_api(data["attendee_name_parts"]),
            attendee_email=data["attendee_email"],
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
    attendee_name: AttendeeNameInput
    attendee_email: str
    answers: Optional[List[AnswerInput]] = None

    def validate(self) -> UpdateAttendeeTicketErrors | None:
        errors = UpdateAttendeeTicketErrors()

        if not self.attendee_email.strip():
            errors.add_error("attendee_email", "This field may not be blank.")

        with errors.with_prefix("attendee_name"):
            self.attendee_name.validate(errors)

        return errors.if_has_errors

    def to_json(self):
        data = {
            "attendee_email": self.attendee_email,
            "attendee_name_parts": self.attendee_name.to_pretix_api(),
        }

        if self.answers is not None:
            data["answers"] = [answer.to_json() for answer in self.answers]

        return data


@strawberry.type
class InvoiceInformationErrors:
    company: list[str] = strawberry.field(default_factory=list)
    given_name: list[str] = strawberry.field(default_factory=list)
    family_name: list[str] = strawberry.field(default_factory=list)
    street: list[str] = strawberry.field(default_factory=list)
    zipcode: list[str] = strawberry.field(default_factory=list)
    city: list[str] = strawberry.field(default_factory=list)
    country: list[str] = strawberry.field(default_factory=list)
    vat_id: list[str] = strawberry.field(default_factory=list)
    fiscal_code: list[str] = strawberry.field(default_factory=list)
    pec: list[str] = strawberry.field(default_factory=list)
    sdi: list[str] = strawberry.field(default_factory=list)


@strawberry.type
class CreateOrderTicketErrors:
    attendee_name: AttendeeNameInputError = strawberry.field(
        default_factory=AttendeeNameInputError
    )
    attendee_email: list[str] = strawberry.field(default_factory=list)


@strawberry.type
class CreateOrderErrors(BaseErrorType):
    @strawberry.type
    class _CreateOrderErrors:
        invoice_information: InvoiceInformationErrors = strawberry.field(
            default_factory=InvoiceInformationErrors
        )
        tickets: list[CreateOrderTicketErrors] = strawberry.field(default_factory=list)
        non_field_errors: list[str] = strawberry.field(default_factory=list)

    errors: _CreateOrderErrors = None


@strawberry.input
class CreateOrderTicketAnswer:
    question_id: str
    value: str


@strawberry.input
class CreateOrderTicket:
    ticket_id: str
    attendee_name: AttendeeNameInput
    attendee_email: str
    variation: Optional[str] = None
    answers: Optional[List[CreateOrderTicketAnswer]] = None
    voucher: Optional[str] = None

    def validate(
        self, errors: CreateOrderErrors, is_admission: bool
    ) -> CreateOrderErrors:
        if not is_admission:
            return errors

        with errors.with_prefix("attendee_name"):
            self.attendee_name.validate(errors)

        if not self.attendee_email.strip():
            errors.add_error("attendee_email", "This field is required")
        elif not validate_email(self.attendee_email):
            errors.add_error("attendee_email", "Invalid email address")

        return errors


@strawberry.input
class InvoiceInformation:
    is_business: bool
    company: Optional[str]
    given_name: str
    family_name: str
    street: str
    zipcode: str
    city: str
    country: str
    vat_id: str
    fiscal_code: str
    pec: str | None = None
    sdi: str | None = None

    def validate(self, errors: CreateOrderErrors) -> CreateOrderErrors:
        required_fields = [
            "given_name",
            "family_name",
            "street",
            "zipcode",
            "city",
            "country",
        ]

        if self.is_business:
            required_fields += ["vat_id", "company"]

        if self.country == "IT":
            if self.is_business:
                required_fields += ["sdi"]
            else:
                required_fields += ["fiscal_code"]

        for required_field in required_fields:
            value = getattr(self, required_field)

            if not value:
                errors.add_error(
                    required_field,
                    "This field is required",
                )

        self.validate_country(errors)

        if self.country == "IT":
            self.validate_italian_zip_code(errors)
            self.validate_pec(errors)

            if self.is_business:
                self.validate_sdi(errors)
                self.validate_partita_iva(errors)
            else:
                self.validate_fiscal_code(errors)

        return errors

    def validate_country(self, errors: CreateOrderErrors):
        if not self.country:
            return

        if not countries.is_valid(self.country):
            errors.add_error(
                "country",
                "Invalid country",
            )

    def validate_pec(self, errors: CreateOrderErrors):
        if not self.pec:
            return

        if not validate_email(self.pec):
            errors.add_error("pec", "Invalid PEC address")

    def validate_fiscal_code(self, errors: CreateOrderErrors):
        if not self.fiscal_code:
            return

        try:
            validate_fiscal_code(self.fiscal_code)
        except FiscalCodeValidationError as exc:
            errors.add_error("fiscal_code", str(exc))

    def validate_partita_iva(self, errors: CreateOrderErrors):
        if not self.vat_id:
            return
        try:
            validate_italian_vat_number(self.vat_id)
        except ItalianVatNumberValidationError as exc:
            errors.add_error("vat_id", str(exc))

    def validate_italian_zip_code(self, errors: CreateOrderErrors):
        if not self.zipcode:
            return

        try:
            validate_italian_zip_code(self.zipcode)
        except ItalianZipCodeValidationError as exc:
            errors.add_error("zipcode", str(exc))

    def validate_sdi(self, errors: CreateOrderErrors):
        if not self.sdi:
            return

        try:
            validate_sdi_code(self.sdi)
        except SdiValidationError as exc:
            errors.add_error("sdi", str(exc))


@strawberry.input
class CreateOrderInput:
    email: str
    locale: str
    payment_provider: str
    invoice_information: InvoiceInformation
    tickets: list[CreateOrderTicket]

    def validate(self, conference) -> CreateOrderErrors:
        # Import here to avoid circular dependency
        from pretix import get_items

        pretix_items = get_items(conference)

        errors = CreateOrderErrors()

        with errors.with_prefix("invoice_information"):
            self.invoice_information.validate(errors)

        for index, ticket in enumerate(self.tickets):
            with errors.with_prefix("tickets", index):
                is_admission = pretix_items[ticket.ticket_id]["admission"]
                ticket.validate(errors, is_admission)

        return errors.if_has_errors


@strawberry.type
class Order:
    code: str
    payment_url: str
