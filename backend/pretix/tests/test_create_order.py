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


@pytest.fixture
def invoice_information():
    return InvoiceInformation(
        is_business=False,
        company="ABC",
        name="ABC",
        street="ABC",
        zipcode="ABC",
        city="ABC",
        country="ABC",
        vat_id="ABC",
        fiscal_code="ABC",
    )


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_creates_order(conference, requests_mock, invoice_information):
    requests_mock.post(
        f"https://pretix/api/organizers/events/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        f"https://pretix/api/organizers/events/questions",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        f"https://pretix/api/organizers/events/items",
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
                attendee_name="Example",
                attendee_email="Example",
                variation=None,
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
@pytest.mark.django_db
def test_raises_when_response_is_400(conference, requests_mock, invoice_information):
    requests_mock.post(
        f"https://pretix/api/organizers/events/orders/", status_code=400, json={}
    )
    requests_mock.get(
        f"https://pretix/api/organizers/events/questions", json={"results": []}
    )
    requests_mock.get(
        f"https://pretix/api/organizers/events/items",
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
                attendee_name="Example",
                attendee_email="Example",
                variation=None,
                answers=None,
            )
        ],
    )

    with pytest.raises(PretixError):
        create_order(conference, order_data)


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_raises_value_error_if_answer_value_is_wrong(
    conference, requests_mock, invoice_information
):
    requests_mock.post(
        f"https://pretix/api/organizers/events/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        f"https://pretix/api/organizers/events/questions",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        f"https://pretix/api/organizers/events/items",
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
                attendee_name="Example",
                attendee_email="Example",
                variation=None,
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
