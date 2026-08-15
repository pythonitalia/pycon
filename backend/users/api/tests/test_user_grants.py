from conferences.tests.factories import ConferenceFactory
from grants.tests.factories import GrantFactory
import pytest


pytestmark = pytest.mark.django_db


def test_query_grant(
    graphql_client,
    user,
):
    conference = ConferenceFactory()

    graphql_client.force_login(user)

    grant = GrantFactory(user_id=user.id, conference=conference)

    response = graphql_client.query(
        """query($conference: String!) {
            me {
                grant(conference: $conference) {
                    id
                }
            }
        }""",
        variables={"conference": conference.code},
    )

    response_grant = response["data"]["me"]["grant"]
    assert int(response_grant["id"]) == grant.id


def test_query_grant_with_no_grant(graphql_client, user):
    conference = ConferenceFactory()

    graphql_client.force_login(user)

    response = graphql_client.query(
        """query($conference: String!) {
            me {
                grant(conference: $conference) {
                    id
                }
            }
        }""",
        variables={"conference": conference.code},
    )

    response_grant = response["data"]["me"]["grant"]
    assert response_grant is None
