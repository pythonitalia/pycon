import pytest

pytestmark = pytest.mark.django_db


def _list_scans_query(graphql_client, variables):
    return graphql_client.query(
        """
        query ListScans($conferenceCode: String!, $page: Int) {
            badgeScans(
                conferenceCode: $conferenceCode,
                page: $page,
            ) {
                pageInfo {
                    totalPages
                    totalItems
                    pageSize
                }
                items {
                    id
                    attendee {
                        fullName
                        email
                    }
                    notes
                }
            }
        }
        """,
        variables=variables,
    )


def test_raises_an_error_when_user_is_not_authenticated(graphql_client, conference):
    resp = _list_scans_query(
        graphql_client,
        variables={"conferenceCode": conference.code},
    )

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"
