from datetime import UTC, datetime, timedelta

from pytest import mark

from conferences.tests.factories import ConferenceFactory
from events.tests.factories import EventFactory

EVENTS_QUERY = """
    query Events($code: String!) {
      conference(code: $code) {
        id
        events {
          id
          conference {
            id
          }
          title
          slug
          content
          locationName
          start
          end
        }
      }
    }
"""


@mark.parametrize("event_count", [1, 4])
@mark.django_db
def test_event_query_with_conference(
    graphql_client,
    django_assert_num_queries,
    event_count,
):
    conference = ConferenceFactory()
    start = datetime(2026, 5, 21, 9, tzinfo=UTC)
    events = EventFactory.create_batch(
        event_count,
        conference=conference,
        start=start,
        end=start + timedelta(hours=1),
    )

    with django_assert_num_queries(2):
        response = graphql_client.query(
            EVENTS_QUERY,
            variables={"code": conference.code},
        )

    assert "errors" not in response
    conference_data = response["data"]["conference"]
    assert conference_data["id"] == str(conference.id)
    assert {event["id"] for event in conference_data["events"]} == {
        str(event.id) for event in events
    }
    assert {event["conference"]["id"] for event in conference_data["events"]} == {
        str(conference.id)
    }
