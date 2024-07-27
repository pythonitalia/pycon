from conferences.tests.factories import ConferenceFactory
from schedule.tests.factories import ScheduleItemFactory
from pytest import mark
from schedule.models import ScheduleItem


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
