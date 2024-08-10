from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin
from django.utils.dateparse import parse_datetime
import requests
from api.types import BaseErrorType
from countries import countries
import strawberry
from django.conf import settings
from django.core.cache import cache
from api.pretix.types import AttendeeNameInput, UpdateAttendeeTicketInput, Voucher
from conferences.models.conference import Conference
from pretix.types import Category, Question, Quota
import sentry_sdk
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

from .exceptions import PretixError

logger = logging.getLogger(__file__)


def get_api_url(conference: Conference, endpoint: str) -> str:
    return urljoin(
        settings.PRETIX_API,
        f"organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/{endpoint}/",  # noqa
    )


def _pretix_request(
    conference: Conference,
    url: str,
    qs: Optional[Dict[str, Any]] = None,
    method="get",
    **kwargs,
):
    return requests.request(
        method,
        url,
        params=qs or {},
        headers={"Authorization": f"Token {settings.PRETIX_API_TOKEN}"},
        **kwargs,
    )


def pretix(
    conference: Conference,
    endpoint: str,
    qs: Optional[Dict[str, Any]] = None,
    method="get",
    **kwargs,
):
    url = get_api_url(conference, endpoint)

    return _pretix_request(conference, url, qs, method, **kwargs)


def get_voucher(conference: Conference, code: str) -> Optional[Voucher]:
    response = pretix(conference, f"extended-vouchers/{code}")

    if response.status_code == 404:
        return None

    response.raise_for_status()
    data = response.json()

    items = []
    all_items = False

    if data["item"]:
        # Only the selected item is included in the voucher
        items = [data["item"]]
    elif data["quota"]:
        # If a quota is specified only items in that quota are valid
        items = data["quota_items"]
    else:
        # No item or quota found
        # it means that this voucher code covers all items
        all_items = True

    return Voucher(
        id=data["id"],
        code=data["code"],
        valid_until=parse_datetime(data["valid_until"])
        if data["valid_until"]
        else None,
        value=data["value"],
        items=items,
        all_items=all_items,
        redeemed=data["redeemed"],
        max_usages=data["max_usages"],
        price_mode=data["price_mode"],
        variation_id=data["variation"],
    )


def create_voucher(
    conference: Conference,
    code: str,
    comment: str,
    tag: str,
    quota_id: int,
    price_mode: str,
    value: str,
):
    payload = {
        "code": code,
        "comment": comment,
        "tag": tag,
        "max_usages": 1,
        "valid_until": None,
        "block_quota": False,
        "allow_ignore_quota": False,
        "price_mode": price_mode,
        "value": value,
        "item": None,
        "variation": None,
        "quota": quota_id,
        "subevent": None,
    }
    response = pretix(conference, "vouchers", method="post", json=payload)
    response.raise_for_status()
    return response.json()


def get_order(conference: Conference, code: str):
    response = pretix(conference, f"orders/{code}")

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()


def get_user_orders(conference: Conference, email: str):
    response = pretix(conference, "orders", {"email": email})
    response.raise_for_status()
    return response.json()


def _get_paginated(
    conference: Conference, endpoint: str, qs: Optional[Dict[str, Any]] = None
):
    url = get_api_url(conference, endpoint)

    while url is not None:
        response = requests.get(
            url,
            params=qs,
            headers={"Authorization": f"Token {settings.PRETIX_API_TOKEN}"},
        )

        response.raise_for_status()

        data = response.json()
        url = data.get("next")

        yield from (order for order in data["results"])


def get_orders(conference: Conference):
    return _get_paginated(conference, "orders")


def get_all_order_positions(
    conference: Conference, params: Optional[Dict[str, Any]] = None
):
    return _get_paginated(conference, "orderpositions", params)


def get_invoices(conference: Conference):
    return _get_paginated(conference, "invoices")


def get_items(conference: Conference, params: Optional[Dict[str, Any]] = None):
    response = pretix(conference, "items", params)
    response.raise_for_status()

    data = response.json()
    return {str(result["id"]): result for result in data["results"]}


def cache_pretix(name: str):
    def factory(func):
        def wrapper(*args, **kwargs):
            conference = args[0]
            cache_key = (
                f"pretix:"
                f"{conference.pretix_organizer_id}:{conference.pretix_event_id}:"
                f"{name}"
            )

            if cache.has_key(cache_key):
                return cache.get(cache_key)

            value = func(*args, **kwargs)
            cache.set(cache_key, value, timeout=60 * 3)
            return value

        return wrapper

    return factory


@cache_pretix(name="questions")
def get_questions(conference: Conference) -> Dict[str, Question]:
    response = pretix(conference, "questions")
    response.raise_for_status()

    data = response.json()
    return {str(result["id"]): result for result in data["results"]}


@cache_pretix(name="categories")
def get_categories(conference: Conference) -> Dict[str, Category]:
    response = pretix(conference, "categories")
    response.raise_for_status()
    data = response.json()
    return {str(result["id"]): result for result in data["results"]}


def get_quotas(conference: Conference) -> Dict[str, Quota]:
    response = pretix(conference, "quotas", qs={"with_availability": "true"})
    response.raise_for_status()

    data = response.json()
    return {str(result["id"]): result for result in data["results"]}


@strawberry.type
class InvoiceInformationErrors:
    company: list[str] = strawberry.field(default_factory=list)
    name: list[str] = strawberry.field(default_factory=list)
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
    attendee_name: list[str] = strawberry.field(default_factory=list)


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

    def validate(self, errors: CreateOrderErrors) -> CreateOrderErrors:
        if not self.attendee_name.validate():
            errors.add_error("attendee_name", "This field is required")

        return errors


@strawberry.input
class InvoiceInformation:
    is_business: bool
    company: Optional[str]
    name: str
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
            "name",
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

        try:
            validate_email(self.pec)
        except ValidationError:
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

    def validate(self) -> CreateOrderErrors:
        errors = CreateOrderErrors()

        with errors.with_prefix("invoice_information"):
            self.invoice_information.validate(errors)

        for index, ticket in enumerate(self.tickets):
            with errors.with_prefix(f"tickets.{index}"):
                ticket.validate(errors)

        return errors.if_has_errors


@strawberry.type
class Order:
    code: str
    payment_url: str


def normalize_answers(ticket: CreateOrderTicket, questions: dict):
    answers = []

    for answer in ticket.answers or []:
        question = questions[answer.question_id]

        if not answer.value and not question.get("required", False):
            continue

        answer_data = {
            "question": answer.question_id,
            "answer": answer.value,
            "options": [],
            "option_identifier": [],
        }

        # TODO: support more question types
        if question["type"] == "C":
            option = next(
                (
                    option
                    for option in question["options"]
                    if str(option["id"]) == answer.value
                ),
                None,
            )

            if option:
                answer_data["options"] = [option["id"]]
                answer_data["option_identifiers"] = [option["identifier"]]
            else:
                raise ValueError("Unable to find option")

        answers.append(answer_data)

    return answers


def normalize_position(ticket: CreateOrderTicket, items: dict, questions: dict):
    item = items[ticket.ticket_id]

    data = {
        "item": ticket.ticket_id,
        "variation": ticket.variation,
        "answers": normalize_answers(ticket, questions),
    }

    if ticket.voucher:
        data["voucher"] = ticket.voucher

    if item["admission"]:
        data["attendee_name_parts"] = ticket.attendee_name.to_pretix_api()
        data["attendee_email"] = ticket.attendee_email

    return data


def create_order(conference: Conference, order_data: CreateOrderInput) -> Order:
    questions = get_questions(conference)
    items = get_items(conference)

    positions = [
        normalize_position(ticket, items, questions) for ticket in order_data.tickets
    ]

    payload = {
        "email": order_data.email,
        "locale": order_data.locale,
        "payment_provider": order_data.payment_provider,
        "testmode": False,
        "positions": positions,
        "invoice_address": {
            "is_business": order_data.invoice_information.is_business,
            "company": order_data.invoice_information.company,
            "name_parts": {"full_name": order_data.invoice_information.name},
            "street": order_data.invoice_information.street,
            "zipcode": order_data.invoice_information.zipcode,
            "city": order_data.invoice_information.city,
            "country": order_data.invoice_information.country,
            "vat_id": order_data.invoice_information.vat_id,
            "internal_reference": order_data.invoice_information.fiscal_code,
        },
    }

    # it needs the / at the end...
    response = pretix(conference, "orders", method="post", json=payload)

    if response.status_code == 400:
        logger.warning("Unable to create order on pretix %s", response.content)

        raise PretixError(response.content.decode("utf-8"))

    response.raise_for_status()

    data = response.json()

    if order_data.invoice_information.country == "IT":
        response = _pretix_request(
            conference,
            urljoin(
                settings.PRETIX_API,
                f"orders/{data['code']}/update_invoice_information/",
            ),
            method="post",
            json={
                "pec": order_data.invoice_information.pec,
                "codice_fiscale": order_data.invoice_information.fiscal_code,
                "sdi": order_data.invoice_information.sdi,
            },
        )

        if response.status_code != 200:
            with sentry_sdk.push_scope() as scope:
                scope.user = {"email": order_data.email}
                scope.set_extra("order-code", data["code"])
                scope.set_extra("pec", order_data.invoice_information.pec)
                scope.set_extra(
                    "codice_fiscale", order_data.invoice_information.fiscal_code
                )
                scope.set_extra("sdi", order_data.invoice_information.sdi)

                sentry_sdk.capture_message(
                    f"Unable to update invoice information for order {data['code']}",
                    level="error",
                )

    return Order(code=data["code"], payment_url=data["payments"][0]["payment_url"])


def user_has_admission_ticket(
    *,
    email: str,
    event_organizer: str,
    event_slug: str,
    additional_events: Optional[List[dict]] = None,
) -> bool:
    additional_events = additional_events or []
    events = [
        {
            "organizer_slug": event_organizer,
            "event_slug": event_slug,
        }
    ] + additional_events
    response = pretix(
        conference=Conference(
            pretix_organizer_id=event_organizer, pretix_event_id=event_slug
        ),
        endpoint="tickets/attendee-has-ticket",
        method="post",
        json={
            "attendee_email": email,
            "events": events,
        },
    )

    response.raise_for_status()

    data = response.json()
    return data["user_has_admission_ticket"]


def get_user_tickets(conference: Conference, email: str):
    response = pretix(
        conference=conference,
        endpoint="tickets/attendee-tickets",
        method="get",
        qs={
            "attendee_email": email,
        },
    )

    response.raise_for_status()

    return response.json()


@cache_pretix(name="all_vouchers")
def get_all_vouchers(conference: Conference):
    vouchers = _get_paginated(conference, "vouchers")
    vouchers_by_id = {voucher["id"]: voucher for voucher in vouchers}
    return vouchers_by_id


def get_user_ticket(conference: Conference, email: str, id: str):
    # TODO: filter by orderposition in the PretixAPI
    tickets = get_user_tickets(conference, email)

    def filter_by(ticket):
        return (
            str(ticket["id"]) == str(id)
            and ticket["attendee_email"].lower() == email.lower()
        )

    tickets = list(filter(filter_by, tickets))

    if tickets:
        return tickets[0]


def is_ticket_owner(conference: Conference, email: str, id: str) -> bool:
    ticket = get_user_ticket(conference, email, id)
    return ticket is not None


def update_ticket(conference: Conference, attendee_ticket: UpdateAttendeeTicketInput):
    response = pretix(
        conference=conference,
        endpoint=f"orderpositions/{attendee_ticket.id}",
        method="PATCH",
        json=attendee_ticket.to_json(),
    )

    response.raise_for_status()

    return response.json()


def get_order_position(conference: Conference, id: str):
    response = pretix(
        conference=conference,
        endpoint=f"orderpositions/{id}",
        method="GET",
    )

    response.raise_for_status()

    return response.json()
