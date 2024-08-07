import datetime
from conferences.tests.factories import (
    ConferenceFactory,
    KeynoteFactory,
    KeynoteSpeakerFactory,
    TopicFactory,
)
from participants.tests.factories import ParticipantFactory
from schedule.tests.factories import (
    DayFactory,
    RoomFactory,
    ScheduleItemFactory,
    SlotFactory,
)
import time_machine
from django.utils import timezone
from pytest import mark

from i18n.strings import LazyI18nString
from schedule.models import DayRoomThroughModel, ScheduleItem


@mark.django_db
def test_get_conference_keynotes_empty(graphql_client):
    conference = ConferenceFactory()

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                keynotes {
                    title(language: "en")
                    speakers {
                        id
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["keynotes"] == []


@mark.django_db
@time_machine.travel("2020-10-10 10:00:00Z", tick=False)
def test_get_conference_keynotes(
    graphql_client,
):
    conference = ConferenceFactory()

    keynote = KeynoteFactory(
        title=LazyI18nString({"en": "title", "it": "titolo"}),
        conference=conference,
        topic=TopicFactory(),
        published=timezone.datetime(
            1995, 12, 1, 5, 10, 3, tzinfo=datetime.timezone.utc
        ),
    )
    speaker = KeynoteSpeakerFactory(keynote=keynote)
    ParticipantFactory(
        user_id=speaker.user_id,
        conference_id=conference.id,
        bio="test",
        photo="https://test.it/test.jpg",
    )

    future_keynote = KeynoteFactory(
        title=LazyI18nString({"en": "nope", "it": "noope"}),
        conference=conference,
        topic=TopicFactory(),
        published=timezone.datetime(
            2050, 12, 1, 5, 10, 3, tzinfo=datetime.timezone.utc
        ),
    )
    KeynoteSpeakerFactory(keynote=future_keynote)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                keynotes {
                    titleEn: title(language: "en")
                    titleIt: title(language: "it")
                    topic {
                        id
                        name
                    }
                    speakers {
                        participant {
                            photo
                        }
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert len(resp["data"]["conference"]["keynotes"]) == 1

    keynote_data = resp["data"]["conference"]["keynotes"][0]

    assert keynote_data["titleEn"] == "title"
    assert keynote_data["titleIt"] == "titolo"
    assert keynote_data["topic"]["id"] == str(keynote.topic.id)
    assert len(keynote_data["speakers"]) == 1

    assert {"participant": {"photo": "https://test.it/test.jpg"}} in keynote_data[
        "speakers"
    ]


@mark.django_db
def test_get_single_conference_keynote(
    graphql_client,
):
    conference = ConferenceFactory()

    keynote = KeynoteFactory(
        slug=LazyI18nString({"en": "title", "it": "titolo"}),
        title=LazyI18nString({"en": "title", "it": "titolo"}),
        conference=conference,
        topic=TopicFactory(),
    )
    speaker = KeynoteSpeakerFactory(keynote=keynote)
    ParticipantFactory(user_id=speaker.user_id, conference_id=conference.id, bio="test")

    resp = graphql_client.query(
        """
        query($code: String!, $slug: String!) {
            conference(code: $code) {
                keynote(slug: $slug) {
                    title(language: "en")
                    topic {
                        id
                        name
                    }
                    speakers {
                        participant {
                            bio
                        }
                    }
                }
            }
        }
        """,
        variables={"code": conference.code, "slug": "title"},
    )

    assert "errors" not in resp

    keynote_data = resp["data"]["conference"]["keynote"]

    assert keynote_data["title"] == "title"
    assert keynote_data["topic"]["id"] == str(keynote.topic.id)
    assert len(keynote_data["speakers"]) == 1

    assert {"participant": {"bio": "test"}} in keynote_data["speakers"]


@mark.django_db
def test_keynote_schedule_info(
    graphql_client,
):
    conference = ConferenceFactory()

    keynote = KeynoteFactory(
        slug=LazyI18nString({"en": "title", "it": "titolo"}),
        title=LazyI18nString({"en": "title", "it": "titolo"}),
        conference=conference,
        topic=TopicFactory(),
    )
    speaker = KeynoteSpeakerFactory(keynote=keynote)
    ParticipantFactory(user_id=speaker.user_id, conference_id=conference.id, bio="test")

    room = RoomFactory(name="Room 1")
    room_2 = RoomFactory(name="Room 2")
    schedule_item = ScheduleItemFactory(
        conference=conference,
        type=ScheduleItem.TYPES.keynote,
        keynote=keynote,
        submission=None,
        slot=SlotFactory(
            day=DayFactory(day=datetime.date(2023, 10, 10), conference=conference),
            hour="10:00",
            duration=30,
        ),
        rooms=[room, room_2],
        youtube_video_id="abc123",
    )
    DayRoomThroughModel.objects.create(
        day=schedule_item.slot.day,
        room=room,
    )
    DayRoomThroughModel.objects.create(
        day=schedule_item.slot.day,
        room=room_2,
    )

    resp = graphql_client.query(
        """
        query($code: String!, $slug: String!) {
            conference(code: $code) {
                keynote(slug: $slug) {
                    start
                    end
                    youtubeVideoId
                    rooms {
                        name
                    }
                }
            }
        }
        """,
        variables={"code": conference.code, "slug": "title"},
    )

    assert "errors" not in resp

    keynote_data = resp["data"]["conference"]["keynote"]
    assert keynote_data["start"] == "2023-10-10T10:00:00"
    assert keynote_data["end"] == "2023-10-10T10:30:00"
    assert keynote_data["youtubeVideoId"] == "abc123"
    assert [room["name"] for room in keynote_data["rooms"]] == ["Room 1", "Room 2"]
