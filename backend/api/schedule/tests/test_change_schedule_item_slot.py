from conferences.tests.factories import ConferenceFactory
import pytest
from django.contrib.admin.models import LogEntry
from schedule.tests.factories import ScheduleItemFactory
from django.contrib.auth.models import Permission


pytestmark = pytest.mark.django_db


def _change_schedule_item_slot(client, **input):
    return client.query(
        """mutation ChangeScheduleItemSlot($input: ChangeScheduleItemSlotInput!) {
        changeScheduleItemSlot(input: $input) {
            id
            items {
                id
                rooms {
                    id
                }
            }
        }
    }""",
        variables={
            "input": input,
        },
    )


@pytest.mark.parametrize("user_to_test", ["admin_user", "user", "not_authenticated"])
def test_without_permissions_cannot_edit_schedule(
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
    rooms = day.added_rooms.all()

    old_room = rooms[0].room
    new_room = rooms[1].room

    slots = day.slots.order_by("hour").all()

    old_slot = slots[0]
    new_slot = slots[1]

    schedule_item = ScheduleItemFactory(conference=conference, slot=old_slot)
    schedule_item.rooms.set([old_room.id])

    response = _change_schedule_item_slot(
        admin_graphql_api_client,
        conferenceId=conference.id,
        scheduleItemId=schedule_item.id,
        newSlotId=new_slot.id,
        rooms=[new_room.id],
    )

    assert response["errors"][0]["message"] == "Cannot edit schedule"
    assert not response.get("data")

    schedule_item.refresh_from_db()
    assert schedule_item.slot_id == old_slot.id
    assert schedule_item.rooms.count() == 1
    assert schedule_item.rooms.first().id == old_room.id

    assert not LogEntry.objects.exists()


def test_cannot_change_schedule_item_of_another_conference(
    admin_graphql_api_client, admin_user, conference_with_schedule_setup
):
    admin_user.admin_conferences.add(ConferenceFactory().id)
    admin_user.user_permissions.add(
        Permission.objects.get(codename="change_scheduleitem")
    )

    admin_graphql_api_client.force_login(admin_user)
    conference = conference_with_schedule_setup

    day = conference.days.first()
    rooms = day.added_rooms.all()

    old_room = rooms[0].room
    new_room = rooms[1].room

    slots = day.slots.order_by("hour").all()

    old_slot = slots[0]
    new_slot = slots[1]

    schedule_item = ScheduleItemFactory(conference=conference, slot=old_slot)
    schedule_item.rooms.set([old_room.id])

    response = _change_schedule_item_slot(
        admin_graphql_api_client,
        conferenceId=conference.id,
        scheduleItemId=schedule_item.id,
        newSlotId=new_slot.id,
        rooms=[new_room.id],
    )

    assert response["errors"][0]["message"] == "Cannot edit schedule"
    assert not response.get("data")

    schedule_item.refresh_from_db()
    assert schedule_item.slot_id == old_slot.id
    assert schedule_item.rooms.count() == 1
    assert schedule_item.rooms.first().id == old_room.id

    assert not LogEntry.objects.exists()


def test_change_schedule_item_slot_and_room(
    admin_graphql_api_client, admin_user, conference_with_schedule_setup
):
    conference = conference_with_schedule_setup

    admin_user.admin_conferences.add(conference.id)
    admin_user.user_permissions.add(
        Permission.objects.get(codename="change_scheduleitem")
    )

    admin_graphql_api_client.force_login(admin_user)

    day = conference.days.first()
    rooms = day.added_rooms.all()

    old_room = rooms[0].room
    new_room = rooms[1].room

    slots = day.slots.order_by("hour").all()

    old_slot = slots[0]
    new_slot = slots[1]

    schedule_item = ScheduleItemFactory(conference=conference, slot=old_slot)
    schedule_item.rooms.set([old_room.id])

    response = _change_schedule_item_slot(
        admin_graphql_api_client,
        conferenceId=conference.id,
        scheduleItemId=schedule_item.id,
        newSlotId=new_slot.id,
        rooms=[new_room.id],
    )

    assert not response.get("errors")
    data = response.get("data")

    assert len(data["changeScheduleItemSlot"]) == 2

    assert data["changeScheduleItemSlot"][0]["id"] == str(old_slot.id)
    assert data["changeScheduleItemSlot"][0]["items"] == []

    assert data["changeScheduleItemSlot"][1]["id"] == str(new_slot.id)
    assert data["changeScheduleItemSlot"][1]["items"][0]["id"] == str(schedule_item.id)
    assert data["changeScheduleItemSlot"][1]["items"][0]["rooms"][0]["id"] == str(
        new_room.id
    )

    schedule_item.refresh_from_db()
    assert schedule_item.slot_id == new_slot.id
    assert schedule_item.rooms.count() == 1
    assert schedule_item.rooms.first().id == new_room.id

    log_entry = LogEntry.objects.get()
    assert log_entry.user_id == admin_user.id
    assert log_entry.object_id == str(schedule_item.id)
    assert log_entry.change_message == (
        f"Changed Slot from {str(old_slot)} to {str(new_slot)} and "
        f"Changed Rooms from {old_room.name} to {new_room.name}"
    )


def test_change_schedule_item_room_only(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)
    conference = conference_with_schedule_setup

    day = conference.days.first()
    rooms = day.added_rooms.all()

    old_room = rooms[0].room
    new_room = rooms[1].room

    old_slot = day.slots.order_by("hour").all()[0]

    schedule_item = ScheduleItemFactory(conference=conference, slot=old_slot)
    schedule_item.rooms.set([old_room.id])

    response = _change_schedule_item_slot(
        admin_graphql_api_client,
        conferenceId=conference.id,
        scheduleItemId=schedule_item.id,
        newSlotId=old_slot.id,
        rooms=[new_room.id],
    )

    assert not response.get("errors")
    data = response.get("data")

    assert len(data["changeScheduleItemSlot"]) == 1

    assert data["changeScheduleItemSlot"][0]["id"] == str(old_slot.id)
    assert data["changeScheduleItemSlot"][0]["items"][0]["id"] == str(schedule_item.id)
    assert data["changeScheduleItemSlot"][0]["items"][0]["rooms"][0]["id"] == str(
        new_room.id
    )

    schedule_item.refresh_from_db()
    assert schedule_item.slot_id == old_slot.id
    assert schedule_item.rooms.count() == 1
    assert schedule_item.rooms.first().id == new_room.id

    log_entry = LogEntry.objects.get()
    assert log_entry.object_id == str(schedule_item.id)
    assert log_entry.change_message == (
        f"Changed Rooms from {old_room.name} to {new_room.name}"
    )


def test_change_schedule_item_slot_only(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)
    conference = conference_with_schedule_setup

    day = conference.days.first()
    rooms = day.added_rooms.all()

    old_room = rooms[0].room

    slots = day.slots.order_by("hour").all()

    old_slot = slots[0]
    new_slot = slots[1]

    schedule_item = ScheduleItemFactory(conference=conference, slot=old_slot)
    schedule_item.rooms.set([old_room.id])

    response = _change_schedule_item_slot(
        admin_graphql_api_client,
        conferenceId=conference.id,
        scheduleItemId=schedule_item.id,
        newSlotId=new_slot.id,
        rooms=[old_room.id],
    )

    assert not response.get("errors")
    data = response.get("data")

    assert len(data["changeScheduleItemSlot"]) == 2

    assert data["changeScheduleItemSlot"][0]["id"] == str(old_slot.id)
    assert data["changeScheduleItemSlot"][0]["items"] == []

    assert data["changeScheduleItemSlot"][1]["id"] == str(new_slot.id)
    assert data["changeScheduleItemSlot"][1]["items"][0]["id"] == str(schedule_item.id)
    assert data["changeScheduleItemSlot"][1]["items"][0]["rooms"][0]["id"] == str(
        old_room.id
    )

    schedule_item.refresh_from_db()
    assert schedule_item.slot_id == new_slot.id
    assert schedule_item.rooms.count() == 1
    assert schedule_item.rooms.first().id == old_room.id

    log_entry = LogEntry.objects.get()
    assert log_entry.object_id == str(schedule_item.id)
    assert log_entry.change_message == (
        f"Changed Slot from {str(old_slot)} to {str(new_slot)}"
    )


def test_move_schedule_item_out_of_slot(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)
    conference = conference_with_schedule_setup

    day = conference.days.first()
    rooms = day.added_rooms.all()

    old_room = rooms[0].room

    slots = day.slots.order_by("hour").all()

    old_slot = slots[0]

    schedule_item = ScheduleItemFactory(conference=conference, slot=old_slot)
    schedule_item.rooms.set([old_room.id])

    response = _change_schedule_item_slot(
        admin_graphql_api_client,
        conferenceId=conference.id,
        scheduleItemId=schedule_item.id,
        newSlotId=None,
        rooms=[],
    )

    assert not response.get("errors")
    data = response.get("data")

    assert len(data["changeScheduleItemSlot"]) == 1

    assert data["changeScheduleItemSlot"][0]["id"] == str(old_slot.id)
    assert data["changeScheduleItemSlot"][0]["items"] == []

    schedule_item.refresh_from_db()
    assert schedule_item.slot_id is None
    assert schedule_item.rooms.count() == 0

    log_entry = LogEntry.objects.get()
    assert log_entry.user_id == admin_superuser.id
    assert log_entry.object_id == str(schedule_item.id)
    assert log_entry.change_message == (
        f"Removed from Slot {str(old_slot)} and "
        f"Removed from Rooms {str(old_room.name)}"
    )


def test_move_schedule_item_to_slot_from_none(
    admin_graphql_api_client, admin_superuser, conference_with_schedule_setup
):
    admin_graphql_api_client.force_login(admin_superuser)
    conference = conference_with_schedule_setup

    day = conference.days.first()
    rooms = day.added_rooms.all()

    new_room = rooms[0].room

    slots = day.slots.order_by("hour").all()

    new_slot = slots[0]

    schedule_item = ScheduleItemFactory(conference=conference, slot=None)
    schedule_item.rooms.set([])

    response = _change_schedule_item_slot(
        admin_graphql_api_client,
        conferenceId=conference.id,
        scheduleItemId=schedule_item.id,
        newSlotId=new_slot.id,
        rooms=[new_room.id],
    )

    assert not response.get("errors")
    data = response.get("data")

    assert len(data["changeScheduleItemSlot"]) == 1

    assert data["changeScheduleItemSlot"][0]["id"] == str(new_slot.id)
    assert data["changeScheduleItemSlot"][0]["items"][0]["id"] == str(schedule_item.id)
    assert data["changeScheduleItemSlot"][0]["items"][0]["rooms"][0]["id"] == str(
        new_room.id
    )

    schedule_item.refresh_from_db()
    assert schedule_item.slot_id == new_slot.id
    assert schedule_item.rooms.count() == 1
    assert schedule_item.rooms.first().id == new_room.id

    log_entry = LogEntry.objects.get()
    assert log_entry.user_id == admin_superuser.id
    assert log_entry.object_id == str(schedule_item.id)
    assert log_entry.change_message == (
        f"Added to Slot {str(new_slot)} and " f"Added to Rooms {str(new_room.name)}"
    )
