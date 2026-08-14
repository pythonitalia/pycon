from pytest import mark

from conferences.tests.factories import ConferenceFactory
from schedule.models import ScheduleItem
from schedule.tests.factories import ScheduleItemFactory


@mark.django_db
def test_get_all_talks(graphql_client):
    conference = ConferenceFactory()
    item = ScheduleItemFactory(
        type=ScheduleItem.TYPES.submission, conference=conference
    )

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
    assert resp["data"]["conference"]["talks"] == [{"title": item.title}]


@mark.django_db
def test_frontend_talks_query_uses_two_queries(
    graphql_client, django_assert_num_queries
):
    conference = ConferenceFactory()
    item = ScheduleItemFactory(
        type=ScheduleItem.TYPES.submission,
        conference=conference,
    )

    with django_assert_num_queries(2):
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
    assert resp["data"]["conference"]["talks"] == [
        {"id": str(item.id), "slug": item.slug}
    ]
