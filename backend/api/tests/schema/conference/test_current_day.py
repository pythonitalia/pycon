from datetime import date, time

import time_machine
from django.utils import timezone
from pytest import mark

from conferences.tests.factories import ConferenceFactory
from schedule.models import ScheduleItem
from schedule.tests.factories import (
    DayFactory,
    RoomFactory,
    ScheduleItemFactory,
    SlotFactory,
)


LIVE_STREAMING_QUERY = """
    query LiveStreamingSection($code: String!) {
        conference(code: $code) {
            id
            timezone
            currentDay {
                day
                runningEvents {
                    id
                    slidoUrl
                    duration
                    title
                    type
                    livestreamingRoom {
                        id
                        name
                    }
                    rooms {
                        id
                        name
                    }
                }
                rooms {
                    id
                    name
                    type
                    streamingUrl
                    slidoUrl
                }
            }
        }
    }
"""


@mark.parametrize("room_count", [1, 4])
@mark.django_db
def test_frontend_header_current_day_query_is_constant(
    graphql_client, django_assert_num_queries, room_count
):
    conference = ConferenceFactory()
    day = DayFactory(conference=conference, day=timezone.localdate())
    for index in range(room_count):
        day.added_rooms.create(
            room=RoomFactory(),
            streaming_url=f"https://streaming.example/{index}",
        )

    with django_assert_num_queries(4):
        resp = graphql_client.query(
            """
            query Header($code: String!) {
                conference(code: $code) {
                    id
                    currentDay {
                        day
                        rooms {
                            id
                            streamingUrl
                        }
                    }
                }
            }
            """,
            variables={"code": conference.code},
        )

    assert "errors" not in resp
    assert len(resp["data"]["conference"]["currentDay"]["rooms"]) == room_count


@mark.parametrize("item_count", [1, 4])
@mark.django_db
@time_machine.travel("2026-06-01 08:30:00Z", tick=False)
def test_frontend_live_streaming_query_returns_latest_running_events(
    graphql_client, django_assert_num_queries, item_count
):
    conference = ConferenceFactory()
    day = DayFactory(conference=conference, day=date(2026, 6, 1))
    room = RoomFactory(name="Main")
    day.added_rooms.create(
        room=room,
        streaming_url="https://streaming.example/main",
        slido_url="https://slido.example/main",
    )
    previous_slot = SlotFactory(day=day, hour=time(9), duration=60)
    current_slot = SlotFactory(day=day, hour=time(10), duration=60)
    previous_item = ScheduleItemFactory(
        conference=conference,
        slot=previous_slot,
        type=ScheduleItem.TYPES.custom,
        title="Previous event",
        duration=60,
        rooms=[room],
        livestreaming_room=room,
        slido_url="https://slido.example/previous",
    )
    current_items = ScheduleItemFactory.create_batch(
        item_count,
        conference=conference,
        slot=current_slot,
        type=ScheduleItem.TYPES.custom,
        duration=60,
        rooms=[room],
        livestreaming_room=room,
        slido_url="https://slido.example/current",
    )

    expected_queries = 9 if item_count == 1 else 8
    with django_assert_num_queries(expected_queries):
        resp = graphql_client.query(
            LIVE_STREAMING_QUERY,
            variables={"code": conference.code},
        )

    assert "errors" not in resp
    running_events = resp["data"]["conference"]["currentDay"]["runningEvents"]
    assert {event["id"] for event in running_events} == {
        str(item.id) for item in current_items
    }
    assert str(previous_item.id) not in {event["id"] for event in running_events}


@mark.django_db
@time_machine.travel("2026-06-01 08:30:00Z", tick=False)
def test_frontend_live_streaming_query_falls_back_from_recruiting_slot(
    graphql_client, django_assert_num_queries
):
    conference = ConferenceFactory()
    day = DayFactory(conference=conference, day=date(2026, 6, 1))
    main_room = RoomFactory(name="Main")
    recruiting_room = RoomFactory(name="Recruiting")
    for room in [main_room, recruiting_room]:
        day.added_rooms.create(
            room=room,
            streaming_url=f"https://streaming.example/{room.id}",
            slido_url=f"https://slido.example/{room.id}",
        )

    previous_slot = SlotFactory(day=day, hour=time(9), duration=60)
    recruiting_slot = SlotFactory(day=day, hour=time(10), duration=60)
    previous_item = ScheduleItemFactory(
        conference=conference,
        slot=previous_slot,
        type=ScheduleItem.TYPES.custom,
        title="Previous event",
        duration=60,
        rooms=[main_room],
        livestreaming_room=main_room,
        slido_url="https://slido.example/previous",
    )
    recruiting_item = ScheduleItemFactory(
        conference=conference,
        slot=recruiting_slot,
        type=ScheduleItem.TYPES.recruiting,
        title="Recruiting",
        duration=60,
        rooms=[recruiting_room],
        livestreaming_room=recruiting_room,
        slido_url="https://slido.example/recruiting",
    )

    with django_assert_num_queries(10):
        resp = graphql_client.query(
            LIVE_STREAMING_QUERY,
            variables={"code": conference.code},
        )

    assert "errors" not in resp
    running_events = resp["data"]["conference"]["currentDay"]["runningEvents"]
    assert [event["id"] for event in running_events] == [str(previous_item.id)]
    assert str(recruiting_item.id) not in {event["id"] for event in running_events}
