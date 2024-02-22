import datetime

from i18n.strings import LazyI18nString
from languages.models import Language
import pytest

from schedule.models import ScheduleItem
from schedule.tests.factories import ScheduleItemFactory
from submissions.tests.factories import SubmissionFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def simple_schedule_item(
    schedule_item_factory, submission_factory, slot_factory, day_factory
):
    submission = submission_factory()

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


@pytest.mark.parametrize("language_code", ["it", "en"])
def test_exposes_abstract_elevator_pitch_in_correct_language(
    graphql_client, user, language_code
):
    graphql_client.force_login(user)

    submission = SubmissionFactory(
        abstract=LazyI18nString({"en": "English abstract", "it": "Italian abstract"}),
        elevator_pitch=LazyI18nString(
            {"en": "English elevator pitch", "it": "Italian elevator pitch"}
        ),
    )

    schedule_item = ScheduleItemFactory(
        status=ScheduleItem.STATUS.confirmed,
        submission=submission,
        type=ScheduleItem.TYPES.talk,
        conference=submission.conference,
        attendees_total_capacity=None,
    )
    schedule_item.language = Language.objects.get(code=language_code)

    response = graphql_client.query(
        """query($slug: String!, $code: String!) {
            conference(code: $code) {
                talk(slug: $slug) {
                    abstract
                    elevatorPitch
                }
            }
        }""",
        variables={"slug": schedule_item.slug, "code": schedule_item.conference.code},
    )

    if language_code == "en":
        assert response["data"]["conference"]["talk"] == {
            "abstract": "English abstract",
            "elevatorPitch": "English elevator pitch",
        }
    else:
        assert response["data"]["conference"]["talk"] == {
            "abstract": "Italian abstract",
            "elevatorPitch": "Italian elevator pitch",
        }


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
