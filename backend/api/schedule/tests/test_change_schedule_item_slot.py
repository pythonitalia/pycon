from schedule.tests.factories import ScheduleItemFactory


def _mutate(client, **input):
    return client.query(
        """mutation ChangeScheduleItemSlot($input: ChangeScheduleItemSlotInput!) {
        changeScheduleItemSlot(input: $input) {
            id
        }
    }""",
        variables={
            "input": input,
        },
    )


def test_change_schedule_item_slot_and_room(
    graphql_client, conference_with_schedule_setup
):
    conference = conference_with_schedule_setup

    day = conference.days.first()
    rooms = day.added_rooms.all()

    first_room = rooms[0]
    last_room = rooms[-1]

    slots = day.slots.order_by("hour").all()

    first_slot = slots[0]
    last_slot = slots[-1]

    schedule_item = ScheduleItemFactory(conference=conference, slot=first_slot)
    schedule_item.rooms.set([first_room.room_id])

    _mutate(
        graphql_client,
        conference_id=conference.id,
        schedule_item_id=schedule_item.id,
        new_slot_id=last_slot.id,
        rooms=[last_room.room.id],
    )
    pass
