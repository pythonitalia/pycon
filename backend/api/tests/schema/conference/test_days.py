from datetime import date, datetime, time

from conferences.tests.factories import ConferenceFactory
from schedule.tests.factories import (
    DayFactory,
    RoomFactory,
    ScheduleItemFactory,
    SlotFactory,
)
from pytest import mark
from pycon.constants import UTC


@mark.django_db
def test_get_days_with_configuration(graphql_client):
    conference = ConferenceFactory(
        start=datetime(2020, 4, 2, tzinfo=UTC),
        end=datetime(2020, 4, 2, tzinfo=UTC),
    )
    day = DayFactory(conference=conference, day=conference.start)

    SlotFactory(day=day, hour=time(8, 45), duration=60)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                days {
                    day
                    slots {
                        hour
                        duration
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["days"] == [
        {"day": "2020-04-02", "slots": [{"hour": "08:45:00", "duration": 60}]}
    ]


@mark.django_db
def test_get_days_items(graphql_client):
    conference = ConferenceFactory(
        start=datetime(2020, 4, 2, tzinfo=UTC),
        end=datetime(2020, 4, 2, tzinfo=UTC),
    )
    day = DayFactory(conference=conference, day=date(2020, 4, 2))

    slot = SlotFactory(day=day, hour=time(8, 45), duration=60)
    slot_2 = SlotFactory(day=day, hour=time(9, 45), duration=60)
    ScheduleItemFactory(conference=conference, slot=slot)
    ScheduleItemFactory(conference=conference, slot=slot_2, image=None)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                days {
                    day
                    slots {
                        items {
                            image
                        }
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    slots = resp["data"]["conference"]["days"][0]["slots"]

    assert slots[0]["items"][0]["image"]
    assert slots[1]["items"][0]["image"] is None


@mark.django_db
def test_days_item_sorted(graphql_client):
    conference = ConferenceFactory(
        start=datetime(2020, 4, 2, tzinfo=UTC),
        end=datetime(2020, 4, 2, tzinfo=UTC),
    )
    day = DayFactory(conference=conference, day=date(2020, 4, 2))

    slot = SlotFactory(day=day, hour=time(8, 45), duration=60)
    slot_2 = SlotFactory(day=day, hour=time(9, 45), duration=60)
    ScheduleItemFactory(conference=conference, slot=slot, type="custom")
    ScheduleItemFactory(conference=conference, slot=slot_2, image=None, type="talk")

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                days {
                    day
                    slots {
                        items {
                            type
                        }
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    slots = resp["data"]["conference"]["days"][0]["slots"]

    assert slots[0]["items"][0]["type"] == "custom"
    assert slots[1]["items"][0]["type"] == "talk"


@mark.django_db
def test_filter_days_by_room(
    graphql_client,
):
    conference = ConferenceFactory(
        start=datetime(2020, 4, 2, tzinfo=UTC),
        end=datetime(2020, 4, 2, tzinfo=UTC),
    )

    day = DayFactory(conference=conference, day=date(2020, 4, 2))

    slot = SlotFactory(day=day, hour=time(8, 45), duration=60)
    slot_2 = SlotFactory(day=day, hour=time(9, 45), duration=60)

    room = RoomFactory(name="Papa John's")
    room_2 = RoomFactory(name="Sushi")

    ScheduleItemFactory(conference=conference, slot=slot, rooms=[room])
    item_2 = ScheduleItemFactory(
        conference=conference, slot=slot_2, image=None, rooms=[room, room_2]
    )

    resp = graphql_client.query(
        """
        query($code: String!, $room: ID) {
            conference(code: $code) {
                days {
                    slots (room: $room) {
                        items {
                            id
                        }
                    }
                }
            }
        }
        """,
        variables={"code": conference.code, "room": room_2.id},
    )

    assert "errors" not in resp
    items = resp["data"]["conference"]["days"][0]["slots"][0]["items"]

    assert len(items) == 1
    assert items[0]["id"] == str(item_2.id)


@mark.django_db
def test_filter_days_by_room_not_found(graphql_client):
    conference = ConferenceFactory(
        start=datetime(2020, 4, 2, tzinfo=UTC),
        end=datetime(2020, 4, 2, tzinfo=UTC),
    )

    day = DayFactory(conference=conference, day=date(2020, 4, 2))

    SlotFactory(day=day, hour=time(8, 45), duration=60)
    SlotFactory(day=day, hour=time(9, 45), duration=60)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                days {
                    slots (room: 1) {
                        items {
                            id
                        }
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert len(resp["data"]["conference"]["days"][0]["slots"]) == 0
