import datetime

import pytest

from schedule.models import ScheduleItem

pytestmark = pytest.mark.django_db


@pytest.fixture
def simple_schedule_item(
    schedule_item_factory, submission_factory, slot_factory, day_factory
):
    submission = submission_factory(
        speaker_id=200,
    )

    return schedule_item_factory(
        status=ScheduleItem.STATUS.confirmed,
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        attendees_total_capacity=None,
        slot=slot_factory(
            day=day_factory(
                day=datetime.date(2020, 10, 10), conference=submission.conference
            ),
            hour=datetime.time(10, 10, 0),
            duration=30,
        ),
        youtube_video_id="AbCdEfGhIjK",
    )


def test_fetch_schedule_talk(simple_schedule_item, graphql_client, user):
    graphql_client.force_login(user)

    schedule_item = simple_schedule_item
    response = graphql_client.query(
        """query($slug: String!, $code: String!) {
            conference(code: $code) {
                talk(slug: $slug) {
                    youtubeVideoId
                    userHasSpot
                    hasSpacesLeft
                    spacesLeft
                }
            }
        }""",
        variables={"slug": schedule_item.slug, "code": schedule_item.conference.code},
    )

    assert response["data"]["conference"]["talk"] == {
        "youtubeVideoId": "AbCdEfGhIjK",
        "userHasSpot": False,
        "hasSpacesLeft": True,
        "spacesLeft": 0,
    }


def test_fetch_custom_event(simple_schedule_item, graphql_client, user):
    graphql_client.force_login(user)

    schedule_item = simple_schedule_item
    schedule_item.type = ScheduleItem.TYPES.custom
    schedule_item.save()

    response = graphql_client.query(
        """query($slug: String!, $code: String!) {
            conference(code: $code) {
                talk(slug: $slug) {
                    userHasSpot
                    hasSpacesLeft
                    spacesLeft
                }
            }
        }""",
        variables={"slug": schedule_item.slug, "code": schedule_item.conference.code},
    )

    assert response["data"]["conference"]["talk"] == {
        "userHasSpot": False,
        "hasSpacesLeft": True,
        "spacesLeft": 0,
    }


def test_fetch_schedule_talk_with_limited_attendees(
    simple_schedule_item, graphql_client, user
):
    graphql_client.force_login(user)

    schedule_item = simple_schedule_item
    schedule_item.attendees_total_capacity = 10
    schedule_item.save()

    response = graphql_client.query(
        """query($slug: String!, $code: String!) {
            conference(code: $code) {
                talk(slug: $slug) {
                    userHasSpot
                    hasSpacesLeft
                    spacesLeft
                }
            }
        }""",
        variables={"slug": schedule_item.slug, "code": schedule_item.conference.code},
    )

    assert response["data"]["conference"]["talk"] == {
        "userHasSpot": False,
        "hasSpacesLeft": True,
        "spacesLeft": 10,
    }
