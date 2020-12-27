from unittest.mock import patch

from pytest import mark


@mark.django_db
def test_logout_user(graphql_client, user):
    graphql_client.force_login(user)

    with patch("api.users.forms.logout") as logout:
        response = graphql_client.query(
            """
        mutation {
            logout {
                __typename

                ... on OperationResult {
                    ok
                }
            }
        }
        """
        )

        logout.assert_called_once()

    assert response["data"]["logout"]["__typename"] == "OperationResult"
    assert response["data"]["logout"]["ok"] is True
