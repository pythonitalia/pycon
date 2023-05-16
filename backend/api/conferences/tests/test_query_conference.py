import pytest
import time_machine
from django.utils import timezone

pytestmark = pytest.mark.django_db


def _query_conference(graphql_client, conference):
    query = """query($code: String!) {
        conference(code: $code) {
            currentDay {
                day
            }
        }
    }"""

    return graphql_client.query(query, variables={"code": conference.code})


def test_query_conference_current_day(conference_factory, graphql_client, day_factory):
    conference = conference_factory()
    day_factory(conference=conference, day=timezone.datetime(2020, 10, 10))
    day_factory(conference=conference, day=timezone.datetime(2020, 10, 11))
    day_factory(conference=conference, day=timezone.datetime(2020, 10, 12))

    with time_machine.travel("2020-10-10 03:00:00Z", tick=False):
        result = _query_conference(graphql_client, conference)
        assert result["data"]["conference"]["currentDay"]["day"] == "2020-10-10"

    with time_machine.travel("2020-10-11 19:00:00Z", tick=False):
        result = _query_conference(graphql_client, conference)
        assert result["data"]["conference"]["currentDay"]["day"] == "2020-10-11"

    with time_machine.travel("2020-10-12 23:00:00Z", tick=False):
        result = _query_conference(graphql_client, conference)
        assert result["data"]["conference"]["currentDay"]["day"] == "2020-10-12"

    with time_machine.travel("2020-10-14 00:00:00Z", tick=False):
        result = _query_conference(graphql_client, conference)
        assert result["data"]["conference"]["currentDay"] is None

    with time_machine.travel("2020-10-04 00:00:00Z", tick=False):
        result = _query_conference(graphql_client, conference)
        assert result["data"]["conference"]["currentDay"] is None
