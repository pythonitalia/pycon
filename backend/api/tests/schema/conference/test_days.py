from datetime import date, datetime, time

from conferences.tests.factories import (
    ConferenceFactory,
    KeynoteFactory,
    KeynoteSpeakerFactory,
)
from participants.tests.factories import ParticipantFactory
from schedule.tests.factories import (
    DayFactory,
    RoomFactory,
    ScheduleItemAttendeeFactory,
    ScheduleItemFactory,
    SlotFactory,
)
from users.tests.factories import UserFactory
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
    ScheduleItemFactory(conference=conference, slot=slot, type="talk")
    ScheduleItemFactory(conference=conference, slot=slot, image=None, type="custom")

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

    assert [item["type"] for item in slots[0]["items"]] == ["custom", "talk"]


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


@mark.django_db
def test_anonymous_user_does_not_have_schedule_spot(graphql_client):
    conference = ConferenceFactory()
    day = DayFactory(conference=conference)
    slot = SlotFactory(day=day, hour=time(8, 45), duration=60)
    ScheduleItemFactory(
        conference=conference,
        slot=slot,
        submission=None,
        type="custom",
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                days {
                    slots {
                        items {
                            userHasSpot
                        }
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["days"][0]["slots"][0]["items"] == [
        {"userHasSpot": False}
    ]


@mark.parametrize("item_count", [1, 4])
@mark.parametrize("item_source", ["submission", "keynote"])
@mark.django_db
def test_schedule_capacity_query_is_constant(
    graphql_client, django_assert_num_queries, item_count, item_source
):
    conference = ConferenceFactory(
        start=datetime(2020, 4, 2, tzinfo=UTC),
        end=datetime(2020, 4, 2, tzinfo=UTC),
    )
    day = DayFactory(conference=conference, day=date(2020, 4, 2))
    slots = [
        SlotFactory(day=day, hour=time(8 + index, 45), duration=60)
        for index in range(item_count)
    ]
    room = RoomFactory(attendees_total_capacity=20)
    items = []
    speakers = []
    for index in range(item_count):
        if item_source == "keynote":
            keynote = KeynoteFactory(conference=conference)
            speaker = KeynoteSpeakerFactory(keynote=keynote).user
            item = ScheduleItemFactory(
                conference=conference,
                slot=slots[index],
                type="keynote",
                submission=None,
                keynote=keynote,
                rooms=[room],
            )
        else:
            item = ScheduleItemFactory(
                conference=conference,
                slot=slots[index],
                type="submission",
                rooms=[room],
            )
            speaker = item.submission.speaker

        ParticipantFactory(conference=conference, user=speaker)
        items.append(item)
        speakers.append(speaker)
    user = UserFactory()
    ScheduleItemAttendeeFactory(schedule_item=items[0], user=user)
    graphql_client.force_login(user)

    expected_queries = 12 if item_source == "keynote" else 10
    with django_assert_num_queries(expected_queries):
        resp = graphql_client.query(
            """
            query($code: String!, $language: String!) {
                conference(code: $code) {
                    id
                    timezone
                    days {
                        day
                        rooms {
                            id
                            name
                            type
                        }
                        slots {
                            id
                            hour
                            endHour
                            duration
                            type
                            items {
                                id
                                title
                                slug
                                type
                                duration
                                hasLimitedCapacity
                                hasSpacesLeft
                                spacesLeft
                                userHasSpot
                                linkTo
                                audienceLevel {
                                    id
                                    name
                                }
                                language {
                                    id
                                    name
                                    code
                                }
                                submission {
                                    id
                                    title(language: $language)
                                }
                                keynote {
                                    id
                                    title(language: "en")
                                }
                                speakers {
                                    id
                                    fullname
                                    participant {
                                        id
                                        photo
                                    }
                                }
                                rooms {
                                    id
                                    name
                                    type
                                }
                            }
                        }
                    }
                }
            }
            """,
            variables={"code": conference.code, "language": "en"},
        )

    assert "errors" not in resp
    schedule_items = [
        item
        for slot in resp["data"]["conference"]["days"][0]["slots"]
        for item in slot["items"]
    ]
    capacity_fields = {
        "id",
        "hasLimitedCapacity",
        "hasSpacesLeft",
        "spacesLeft",
        "userHasSpot",
    }
    assert {field: schedule_items[0][field] for field in capacity_fields} == {
        "id": str(items[0].id),
        "hasLimitedCapacity": True,
        "hasSpacesLeft": True,
        "spacesLeft": 19,
        "userHasSpot": True,
    }
    assert [
        {field: schedule_item[field] for field in capacity_fields}
        for schedule_item in schedule_items[1:]
    ] == [
        {
            "id": str(item.id),
            "hasLimitedCapacity": True,
            "hasSpacesLeft": True,
            "spacesLeft": 20,
            "userHasSpot": False,
        }
        for item in items[1:]
    ]
    assert [schedule_item["speakers"][0]["id"] for schedule_item in schedule_items] == [
        str(speaker.id) for speaker in speakers
    ]
    assert all(
        schedule_item["speakers"][0]["participant"] for schedule_item in schedule_items
    )
