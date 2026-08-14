from django.utils import timezone
from pytest import mark

from conferences.tests.factories import ConferenceFactory
from schedule.tests.factories import DayFactory, RoomFactory


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
