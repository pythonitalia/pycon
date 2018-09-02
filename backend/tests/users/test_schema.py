def test_fails_when_user_is_not_authenticated(graphql_client):
    resp = graphql_client.query(
        """
        {
            me {
                email
            }
        }
        """
    )

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


def test_works_when_user_is_logged_in(user, graphql_client):
    graphql_client.force_login(user)

    resp = graphql_client.query(
        """
        {
            me {
                email
            }
        }
        """
    )

    assert "errors" not in resp
    assert resp["data"]["me"]["email"] == user.email
