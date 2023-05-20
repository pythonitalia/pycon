import pytest
from badge_scanner.models import BadgeScan

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


def test_returns_only_scans_by_current_user(user, graphql_client, conference, mocker):
    graphql_client.force_login(user)

    scan = BadgeScan.objects.create(
        scanned_by_id=user.id,
        conference=conference,
        scanned_user_id=1,
        badge_url="https://foo.bar",
        notes="",
    )

    BadgeScan.objects.create(
        scanned_by_id=2,
        conference=conference,
        scanned_user_id=1,
        badge_url="https://foo.bar",
        notes="",
    )

    resp = _list_scans_query(
        graphql_client,
        variables={"conferenceCode": conference.code},
    )

    assert resp["data"]["badgeScans"] == {
        "pageInfo": {"totalPages": 1, "totalItems": 1, "pageSize": 100},
        "items": [{"id": str(scan.id)}],
    }
