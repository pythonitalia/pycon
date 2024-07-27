from conferences.tests.factories import ConferenceFactory
from hotels.tests.factories import BedLayoutFactory, HotelRoomFactory
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


pytestmark = pytest.mark.django_db


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
def test_creates_order(requests_mock, invoice_information):
    conference = ConferenceFactory()
    bed_layout = BedLayoutFactory()
    hotel_room = HotelRoomFactory(conference=conference)
    hotel_room.conference = conference
    hotel_room.available_bed_layouts.add(bed_layout)
    hotel_room.save()

    requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items",
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
                bed_layout_id=str(bed_layout.id),
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
def test_raises_when_response_is_400(requests_mock, invoice_information):
    conference = ConferenceFactory()
    requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        status_code=400,
        json={},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions",
        json={"results": []},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items",
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
def test_raises_value_error_if_answer_value_is_wrong(
    requests_mock, invoice_information
):
    conference = ConferenceFactory()
    requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items",
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


def test_create_hotel_positions():
    room = HotelRoomFactory(
        conference__pretix_hotel_ticket_id=1,
        conference__pretix_hotel_room_type_question_id=2,
        conference__pretix_hotel_checkin_question_id=3,
        conference__pretix_hotel_checkout_question_id=4,
        conference__pretix_hotel_bed_layout_question_id=5,
        price=100,
    )
    bed_layout = BedLayoutFactory()
    room.available_bed_layouts.add(bed_layout)

    rooms = [
        CreateOrderHotelRoom(
            room_id=str(room.id),
            checkin=timezone.datetime(2020, 1, 1).date(),
            checkout=timezone.datetime(2020, 1, 3).date(),
            bed_layout_id=str(bed_layout.id),
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
                {
                    "question": 5,
                    "answer": bed_layout.name.localize("en"),
                    "options": [],
                    "option_identifier": [],
                },
            ],
        }
    ]


@override_settings(PRETIX_API="https://pretix/api/")
def test_not_required_and_empty_answer_is_skipped(requests_mock, invoice_information):
    conference = ConferenceFactory()
    orders_mock = requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )

    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions",
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
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items",
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
def test_create_order_with_positions_with_voucher_and_one_without(
    requests_mock, invoice_information
):
    conference = ConferenceFactory()
    orders_mock = requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items",
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


@override_settings(PRETIX_API="https://pretix/api/")
def test_creates_order_with_additional_info_for_e_invoice(requests_mock):
    conference = ConferenceFactory()
    bed_layout = BedLayoutFactory()
    hotel_room = HotelRoomFactory(conference=conference)
    hotel_room.available_bed_layouts.add(bed_layout)
    hotel_room.save()

    requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items",
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
            name="ABC",
            street="ABC",
            zipcode="ABC",
            city="ABC",
            country="IT",
            vat_id="ABC",
            fiscal_code="ABC",
            pec="example@example.com",
            sdi="1231231",
        ),
        hotel_rooms=[
            CreateOrderHotelRoom(
                room_id=str(hotel_room.id),
                checkin=timezone.datetime(2020, 1, 1).date(),
                checkout=timezone.datetime(2020, 1, 3).date(),
                bed_layout_id=str(bed_layout.id),
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
def test_creates_order_with_additional_info_for_e_invoice_does_not_break_on_error(
    requests_mock,
):
    conference = ConferenceFactory()
    hotel_room = HotelRoomFactory(conference=conference)
    bed_layout = BedLayoutFactory()
    hotel_room.available_bed_layouts.add(bed_layout)
    hotel_room.save()

    requests_mock.post(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/orders/",
        json={"payments": [{"payment_url": "http://example.com"}], "code": 123},
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/questions",
        json={
            "results": [
                {"id": "1", "type": "S"},
                {"id": "2", "type": "C", "options": [{"id": 1, "identifier": "abc"}]},
            ]
        },
    )
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/items",
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
            name="ABC",
            street="ABC",
            zipcode="ABC",
            city="ABC",
            country="IT",
            vat_id="ABC",
            fiscal_code="ABC",
            pec="example@example.com",
            sdi="1231231",
        ),
        hotel_rooms=[
            CreateOrderHotelRoom(
                room_id=str(hotel_room.id),
                checkin=timezone.datetime(2020, 1, 1).date(),
                checkout=timezone.datetime(2020, 1, 3).date(),
                bed_layout_id=str(bed_layout.id),
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
