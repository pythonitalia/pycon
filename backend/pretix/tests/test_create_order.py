import pytest
from django.test import override_settings
from django.utils import timezone
from pretix import (
    CreateOrderHotelRoom,
    CreateOrderInput,
    CreateOrderTicket,
    CreateOrderTicketAnswer,
    InvoiceInformation,
    create_hotel_positions,
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
def test_creates_order(conference, hotel_room, requests_mock, invoice_information):
    hotel_room.conference = conference
    hotel_room.save()

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
        hotel_rooms=[
            CreateOrderHotelRoom(
                room_id=str(hotel_room.id),
                checkin=timezone.datetime(2020, 1, 1).date(),
                checkout=timezone.datetime(2020, 1, 3).date(),
            )
        ],
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name="Example",
                attendee_email="Example",
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
        hotel_rooms=[],
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name="Example",
                attendee_email="Example",
                variation=None,
                answers=None,
                voucher=None,
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
        hotel_rooms=[],
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name="Example",
                attendee_email="Example",
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


@pytest.mark.django_db
def test_create_hotel_positions(requests_mock, hotel_room_factory, invoice_information):
    room = hotel_room_factory(
        conference__pretix_hotel_ticket_id=1,
        conference__pretix_hotel_room_type_question_id=2,
        conference__pretix_hotel_checkin_question_id=3,
        conference__pretix_hotel_checkout_question_id=4,
        price=100,
    )

    rooms = [
        CreateOrderHotelRoom(
            room_id=str(room.id),
            checkin=timezone.datetime(2020, 1, 1).date(),
            checkout=timezone.datetime(2020, 1, 3).date(),
        )
    ]

    positions = create_hotel_positions(rooms, "en", room.conference)

    assert positions == [
        {
            "item": 1,
            "price": "200.00",
            "answers": [
                {
                    "question": 2,
                    "answer": room.name.localize("en"),
                    "options": [],
                    "option_identifier": [],
                },
                {
                    "question": 3,
                    "answer": "2020-01-01",
                    "options": [],
                    "option_identifier": [],
                },
                {
                    "question": 4,
                    "answer": "2020-01-03",
                    "options": [],
                    "option_identifier": [],
                },
            ],
        }
    ]


@override_settings(PRETIX_API="https://pretix/api/")
@pytest.mark.django_db
def test_not_required_and_empty_answer_is_skipped(
    conference, requests_mock, invoice_information
):
    orders_mock = requests_mock.post(
        f"https://pretix/api/organizers/events/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )

    requests_mock.get(
        f"https://pretix/api/organizers/events/questions",
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
        f"https://pretix/api/organizers/events/items",
        json={"results": [{"id": "123", "admission": True}]},
    )

    order_data = CreateOrderInput(
        email="my@email.com",
        locale="en",
        payment_provider="stripe",
        invoice_information=invoice_information,
        hotel_rooms=[],
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name="Example",
                attendee_email="Example",
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
@pytest.mark.django_db
def test_create_order_with_positions_with_voucher_and_one_without(
    conference, requests_mock, invoice_information
):
    orders_mock = requests_mock.post(
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
        hotel_rooms=[],
        tickets=[
            CreateOrderTicket(
                ticket_id="123",
                attendee_name="Example",
                attendee_email="Example",
                variation=None,
                voucher=None,
                answers=[
                    CreateOrderTicketAnswer(question_id="1", value="ABC"),
                    CreateOrderTicketAnswer(question_id="2", value="1"),
                ],
            ),
            CreateOrderTicket(
                ticket_id="123",
                attendee_name="Example",
                attendee_email="Example",
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
