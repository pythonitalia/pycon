import pytest

from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


def test_logout(full_response_graphql_client):
    user = UserFactory(
        email="reset@example.org", password="old-password", jwt_auth_id=1
    )
    full_response_graphql_client.force_login(user)

    body, response = full_response_graphql_client.query(
        """mutation {
            logout {
                __typename
                ... on OperationSuccess {
                    ok
                }
            }
        }""",
        variables={},
    )

    assert body["data"]["logout"]["ok"] is True
    assert response.cookies["pythonitalia_sessionid"].value == ""
