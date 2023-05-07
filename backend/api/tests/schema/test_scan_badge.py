def _scan_badge_mutation(graphql_client, variables):
    return graphql_client.query(
        """
        mutation ScanBadge($url: String!) {
            scanBadge(input: { url: $url }) {
                __typename
                ... on BadgeScan {
                    attendee {
                        fullName
                        email
                    }
                    notes
                }
                ... on ScanError {
                    message
                }
            }
        }
        """,
        variables=variables,
    )


def test_raises_an_error_when_user_is_not_authenticated(graphql_client):
    resp = _scan_badge_mutation(graphql_client, variables={"url": "https://foo.bar"})

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


# TODO: make sure the user is a sponsor


def test_works_when_user_is_logged_in(user, graphql_client):
    graphql_client.force_login(user)

    # TODO: mock the pretix API ?

    resp = _scan_badge_mutation(
        graphql_client, variables={"url": "https://pycon.it/profile/this-is-a-test"}
    )

    assert "errors" not in resp
    assert resp["data"]["scanBadge"]["__typename"] == "BadgeScan"
    assert resp["data"]["scanBadge"]["attendee"]["fullName"] == "Test User"
    assert resp["data"]["scanBadge"]["attendee"]["email"] == "some@email.com"
    assert resp["data"]["scanBadge"]["notes"] is None
