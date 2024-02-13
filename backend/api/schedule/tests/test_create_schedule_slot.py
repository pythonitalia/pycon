from datetime import time
from django.contrib.admin.models import LogEntry
import pytest
from schedule.models import Slot
from schedule.tests.factories import SlotFactory

pytestmark = pytest.mark.django_db


def _create_schedule_slot(client, **input):
    return client.query(
        """mutation CreateScheduleSlot($input: CreateScheduleSlotInput!) {
        createScheduleSlot(input: $input) {
            id
            slots {
                hour
                duration
            }
        }
    }""",
        variables={
            "input": input,
        },
    )


@pytest.mark.parametrize("user_to_test", ["admin_user", "user", "not_authenticated"])
def test_cannot_create_schedule_slot_with_no_permissions(
    admin_graphql_api_client,
    user_to_test,
    user,
    admin_user,
    conference_with_schedule_setup,
):
    if user_to_test == "admin_user":
        admin_graphql_api_client.force_login(admin_user)
    elif user_to_test == "user":
        admin_graphql_api_client.force_login(user)

    conference = conference_with_schedule_setup
    day = conference.days.first()
    day.slots.all().delete()

    response = _create_schedule_slot(
        admin_graphql_api_client,
        conferenceId=conference.id,
        dayId=day.id,
        duration=30,
        type=Slot.TYPES.default,
    )

    assert response["errors"][0]["message"] == "Cannot edit schedule"
    assert not response.get("data")

    day.refresh_from_db()
    assert day.slots.count() == 0

    assert LogEntry.objects.count() == 0


def test_create_schedule_slot_with_no_previous_slot(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)

    conference = conference_with_schedule_setup
    day = conference.days.first()
    day.slots.all().delete()

    response = _create_schedule_slot(
        admin_graphql_api_client,
        conferenceId=conference.id,
        dayId=day.id,
        duration=30,
        type=Slot.TYPES.default,
    )

    assert not response.get("errors")
    data = response["data"]

    assert data["createScheduleSlot"]["id"] == str(day.id)
    assert data["createScheduleSlot"]["slots"] == [{"hour": "09:15:00", "duration": 30}]

    conference.refresh_from_db()
    day.refresh_from_db()

    assert day.slots.count() == 1

    slot = day.slots.first()
    assert slot.duration == 30
    assert slot.type == Slot.TYPES.default
    assert slot.hour == time(9, 15)

    log_entry = LogEntry.objects.get()
    assert log_entry.user_id == admin_superuser.id
    assert log_entry.change_message == "Created Slot 09:15:00 [30]"


def test_create_schedule_slot_with_previous_slot(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)

    conference = conference_with_schedule_setup
    day = conference.days.first()
    day.slots.all().delete()
    SlotFactory(
        day=day,
        hour=time(9, 0),
        duration=10,
    )

    response = _create_schedule_slot(
        admin_graphql_api_client,
        conferenceId=conference.id,
        dayId=day.id,
        duration=20,
        type=Slot.TYPES["break"],
    )

    assert not response.get("errors")
    data = response["data"]

    assert data["createScheduleSlot"]["id"] == str(day.id)
    assert data["createScheduleSlot"]["slots"] == [
        {"hour": "09:00:00", "duration": 10},
        {"hour": "09:10:00", "duration": 20},
    ]

    conference.refresh_from_db()
    day.refresh_from_db()

    assert day.slots.count() == 2

    slot = day.slots.order_by("hour").last()
    assert slot.duration == 20
    assert slot.type == Slot.TYPES["break"]
    assert slot.hour == time(9, 10)


def test_create_schedule_slot_with_many_previous_slots(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)

    conference = conference_with_schedule_setup
    day = conference.days.first()
    day.slots.all().delete()
    SlotFactory(
        day=day,
        hour=time(9, 0),
        duration=10,
    )

    SlotFactory(
        day=day,
        hour=time(9, 20),
        duration=10,
    )

    SlotFactory(
        day=day,
        hour=time(9, 10),
        duration=10,
    )

    response = _create_schedule_slot(
        admin_graphql_api_client,
        conferenceId=conference.id,
        dayId=day.id,
        duration=20,
        type=Slot.TYPES["break"],
    )

    assert not response.get("errors")
    data = response["data"]

    assert data["createScheduleSlot"]["id"] == str(day.id)
    assert data["createScheduleSlot"]["slots"] == [
        {"hour": "09:00:00", "duration": 10},
        {"hour": "09:10:00", "duration": 10},
        {"hour": "09:20:00", "duration": 10},
        {"hour": "09:30:00", "duration": 20},
    ]

    conference.refresh_from_db()
    day.refresh_from_db()

    assert day.slots.count() == 4

    slot = day.slots.order_by("hour").last()
    assert slot.duration == 20
    assert slot.type == Slot.TYPES["break"]
    assert slot.hour == time(9, 30)
