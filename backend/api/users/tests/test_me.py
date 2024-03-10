from association_membership.enums import MembershipStatus
from association_membership.models import Membership
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


def test_is_python_italia_member_user_without_membership(graphql_client, user):
    graphql_client.force_login(user)
    response = graphql_client.query(
        """query {
        me {
            isPythonItaliaMember
        }
    }"""
    )

    me = response["data"]["me"]
    assert me["isPythonItaliaMember"] is False


def test_is_python_italia_member_with_membership_exists_and_active(
    graphql_client, user
):
    Membership.objects.create(user=user, status=MembershipStatus.ACTIVE)

    graphql_client.force_login(user)
    response = graphql_client.query(
        """query {
        me {
            isPythonItaliaMember
        }
    }"""
    )

    me = response["data"]["me"]
    assert me["isPythonItaliaMember"] is True


@pytest.mark.parametrize(
    "status", [MembershipStatus.CANCELED, MembershipStatus.PENDING]
)
def test_is_python_italia_member_with_expired_membership(graphql_client, user, status):
    Membership.objects.create(user=user, status=status)

    graphql_client.force_login(user)
    response = graphql_client.query(
        """query {
        me {
            isPythonItaliaMember
        }
    }"""
    )

    me = response["data"]["me"]
    assert me["isPythonItaliaMember"] is False
