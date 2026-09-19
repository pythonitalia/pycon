from pytest import mark

from conferences.tests.factories import ConferenceFactory
from schedule.models import ScheduleItem
from schedule.tests.factories import ScheduleItemFactory


@mark.django_db
def test_get_all_talks_is_always_empty(graphql_client):
    conference = ConferenceFactory()
    ScheduleItemFactory(type=ScheduleItem.TYPES.talk, conference=conference)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                talks {
                    title
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["talks"] == []


@mark.django_db
def test_frontend_talks_query_only_looks_up_the_conference(
    graphql_client, django_assert_num_queries
):
    conference = ConferenceFactory()
    ScheduleItemFactory(type=ScheduleItem.TYPES.talk, conference=conference)

    # talks resolves to an empty queryset, so it never hits the database
    with django_assert_num_queries(1):
        resp = graphql_client.query(
            """
            query AllTalks($code: String!) {
                conference(code: $code) {
                    id
                    talks {
                        id
                        slug
                    }
                }
            }
            """,
            variables={"code": conference.code},
        )

    assert "errors" not in resp
    assert resp["data"]["conference"]["talks"] == []
