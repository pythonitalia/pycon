from conferences.tests.factories import ConferenceFactory
import pytest

pytestmark = pytest.mark.django_db


def test_user_schedule_favourites_calendar_url(graphql_client, user):
    conference = ConferenceFactory()
    graphql_client.force_login(user)
    response = graphql_client.query(
        """query($conference: String!) {
        me {
            userScheduleFavouritesCalendarUrl(conference: $conference)
        }
    }""",
        variables={
            "conference": conference.code,
        },
    )

    me = response["data"]["me"]
    assert (
        f"/schedule/user-schedule-favourites-calendar/{conference.id}/{user.user_hashid()}?sh="
        in me["userScheduleFavouritesCalendarUrl"]
    )


def test_user_schedule_favourites_calendar_url_fails_with_invalid_conference(
    graphql_client, user
):
    graphql_client.force_login(user)
    response = graphql_client.query(
        """query($conference: String!) {
        me {
            userScheduleFavouritesCalendarUrl(conference: $conference)
        }
    }""",
        variables={
            "conference": "invalid",
        },
    )

    me = response["data"]["me"]
    assert me["userScheduleFavouritesCalendarUrl"] is None
