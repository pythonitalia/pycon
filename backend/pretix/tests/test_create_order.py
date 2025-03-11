from api.pretix.types import AttendeeNameInput
from conferences.tests.factories import ConferenceFactory
import pytest
from django.test import override_settings

from pretix import (
    CreateOrderInput,
    CreateOrderTicket,
    CreateOrderTicketAnswer,
    InvoiceInformation,
    create_order,
)
from pretix.exceptions import PretixError


pytestmark = pytest.mark.django_db


@pytest.fixture
def invoice_information():
    return InvoiceInformation(
        is_business=False,
        company="ABC",
        first_name="Patrick",
        last_name="Arminio",
        street="ABC",
        zipcode="ABC",
        city="ABC",
        country="ABC",
        vat_id="ABC",
        fiscal_code="ABC",
    )


@override_settings(PRETIX_API="https://pretix/api/")
def test_creates_order(requests_mock, invoice_information):
    conference = ConferenceFactory()

    requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions/",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items/",
        json={"results": [{"id": "123", "admission": True}]},
    )

    order_data = CreateOrderInput(
        email="my@email.com",
        locale="en",
        payment_provider="stripe",
        invoice_information=invoice_information,
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name=AttendeeNameInput(
                    scheme="given_family",
                    parts={"given_name": "John", "family_name": "Doe"},
                ),
                attendee_email="example@example.org",
                variation=None,
                voucher=None,
                answers=[
                    CreateOrderTicketAnswer(question_id="1", value="ABC"),
                    CreateOrderTicketAnswer(question_id="2", value="1"),
                ],
            )
        ],
    )

    result = create_order(conference, order_data)

    assert result.payment_url == "http://example.com"


@override_settings(PRETIX_API="https://pretix/api/")
def test_raises_when_response_is_400(requests_mock, invoice_information):
    conference = ConferenceFactory()
    requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        status_code=400,
        json={},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions/",
        json={"results": []},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items/",
        json={"results": [{"id": "123", "admission": False}]},
    )

    order_data = CreateOrderInput(
        email="my@email.com",
        locale="en",
        payment_provider="stripe",
        invoice_information=invoice_information,
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name=AttendeeNameInput(
                    scheme="given_family",
                    parts={"given_name": "John", "family_name": "Doe"},
                ),
                attendee_email="example@example.org",
                variation=None,
                answers=None,
                voucher=None,
            )
        ],
    )

    with pytest.raises(PretixError):
        create_order(conference, order_data)


@override_settings(PRETIX_API="https://pretix/api/")
def test_raises_value_error_if_answer_value_is_wrong(
    requests_mock, invoice_information
):
    conference = ConferenceFactory()
    requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions/",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items/",
        json={"results": [{"id": "123", "admission": True}]},
    )

    order_data = CreateOrderInput(
        email="my@email.com",
        locale="en",
        payment_provider="stripe",
        invoice_information=invoice_information,
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name=AttendeeNameInput(
                    scheme="given_family",
                    parts={"given_name": "John", "family_name": "Doe"},
                ),
                attendee_email="example@example.org",
                variation=None,
                voucher=None,
                answers=[
                    CreateOrderTicketAnswer(question_id="1", value="ABC"),
                    # 100 doesn't exist as id in the questions
                    CreateOrderTicketAnswer(question_id="2", value="100"),
                ],
            )
        ],
    )

    with pytest.raises(ValueError):
        create_order(conference, order_data)


@override_settings(PRETIX_API="https://pretix/api/")
def test_not_required_and_empty_answer_is_skipped(requests_mock, invoice_information):
    conference = ConferenceFactory()
    orders_mock = requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )

    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions/",
        json={
            "results": [
                {"id": "1", "type": "S", "required": False},
                {
                    "id": "2",
                    "type": "C",
                    "required": True,
                    "options": [{"id": 1, "identifier": "abc"}],
                },
            ]
        },
    )

    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items/",
        json={"results": [{"id": "123", "admission": True}]},
    )

    order_data = CreateOrderInput(
        email="my@email.com",
        locale="en",
        payment_provider="stripe",
        invoice_information=invoice_information,
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name=AttendeeNameInput(
                    scheme="given_family",
                    parts={"given_name": "John", "family_name": "Doe"},
                ),
                attendee_email="example@example.org",
                variation=None,
                voucher=None,
                answers=[
                    CreateOrderTicketAnswer(question_id="1", value=""),
                    CreateOrderTicketAnswer(question_id="2", value="1"),
                ],
            )
        ],
    )

    result = create_order(conference, order_data)

    assert result.payment_url == "http://example.com"

    body = orders_mock.request_history[0].json()
    answers = body["positions"][0]["answers"]

    assert len(answers) == 1
    assert answers == [
        {
            "question": "2",
            "answer": "1",
            "options": [1],
            "option_identifier": [],
            "option_identifiers": ["abc"],
        }
    ]


@override_settings(PRETIX_API="https://pretix/api/")
def test_create_order_with_positions_with_voucher_and_one_without(
    requests_mock, invoice_information
):
    conference = ConferenceFactory()
    orders_mock = requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions/",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items/",
        json={"results": [{"id": "123", "admission": True}]},
    )

    order_data = CreateOrderInput(
        email="my@email.com",
        locale="en",
        payment_provider="stripe",
        invoice_information=invoice_information,
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name=AttendeeNameInput(
                    scheme="given_family",
                    parts={"given_name": "John", "family_name": "Doe"},
                ),
                attendee_email="example@example.org",
                variation=None,
                voucher=None,
                answers=[
                    CreateOrderTicketAnswer(question_id="1", value="ABC"),
                    CreateOrderTicketAnswer(question_id="2", value="1"),
                ],
            ),
            CreateOrderTicket(
                ticket_id="123",
                attendee_name=AttendeeNameInput(
                    scheme="given_family",
                    parts={"given_name": "John", "family_name": "Doe"},
                ),
                attendee_email="example@example.org",
                variation=None,
                voucher="friendly-human-being",
                answers=[
                    CreateOrderTicketAnswer(question_id="1", value="ABC"),
                    CreateOrderTicketAnswer(question_id="2", value="1"),
                ],
            ),
        ],
    )

    result = create_order(conference, order_data)

    assert result.payment_url == "http://example.com"

    body = orders_mock.request_history[0].json()
    assert "voucher" not in body["positions"][0]
    assert body["positions"][1]["voucher"] == "friendly-human-being"


@override_settings(PRETIX_API="https://pretix/api/")
def test_creates_order_with_additional_info_for_e_invoice(requests_mock):
    conference = ConferenceFactory()

    requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions/",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items/",
        json={"results": [{"id": "123", "admission": True}]},
    )

    requests_mock.post(
        "https://pretix/api/orders/123/update_invoice_information/",
        json={},
    )

    order_data = CreateOrderInput(
        email="my@email.com",
        locale="en",
        payment_provider="stripe",
        invoice_information=InvoiceInformation(
            is_business=False,
            company="ABC",
            first_name="Patrick",
            last_name="Arminio",
            street="ABC",
            zipcode="ABC",
            city="ABC",
            country="IT",
            vat_id="ABC",
            fiscal_code="ABC",
            pec="example@example.com",
            sdi="1231231",
        ),
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name=AttendeeNameInput(
                    scheme="given_family",
                    parts={"given_name": "John", "family_name": "Doe"},
                ),
                attendee_email="example@example.org",
                variation=None,
                voucher=None,
                answers=[
                    CreateOrderTicketAnswer(question_id="1", value="ABC"),
                    CreateOrderTicketAnswer(question_id="2", value="1"),
                ],
            )
        ],
    )

    result = create_order(conference, order_data)

    assert result.payment_url == "http://example.com"


@override_settings(PRETIX_API="https://pretix/api/")
def test_creates_order_with_additional_info_for_e_invoice_does_not_break_on_error(
    requests_mock,
):
    conference = ConferenceFactory()

    requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions/",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items/",
        json={"results": [{"id": "123", "admission": True}]},
    )

    requests_mock.post(
        "https://pretix/api/orders/123/update_invoice_information/",
        json={},
        status_code=400,
    )

    order_data = CreateOrderInput(
        email="my@email.com",
        locale="en",
        payment_provider="stripe",
        invoice_information=InvoiceInformation(
            is_business=False,
            company="ABC",
            first_name="Patrick",
            last_name="Arminio",
            street="ABC",
            zipcode="ABC",
            city="ABC",
            country="IT",
            vat_id="ABC",
            fiscal_code="ABC",
            pec="example@example.com",
            sdi="1231231",
        ),
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name=AttendeeNameInput(
                    scheme="given_family",
                    parts={"given_name": "John", "family_name": "Doe"},
                ),
                attendee_email="example@example.org",
                variation=None,
                voucher=None,
                answers=[
                    CreateOrderTicketAnswer(question_id="1", value="ABC"),
                    CreateOrderTicketAnswer(question_id="2", value="1"),
                ],
            )
        ],
    )

    result = create_order(conference, order_data)

    assert result.payment_url == "http://example.com"
