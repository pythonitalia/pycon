from users.tests.factories import UserFactory
from conferences.tests.factories import ConferenceFactory
import pytest
from badge_scanner.models import BadgeScan

pytestmark = pytest.mark.django_db


def _get_scan_query(graphql_client, variables):
    return graphql_client.query(
        """
        query GetScan($id: ID!) {
            badgeScan(id: $id) {
                id
            }
        }
        """,
        variables=variables,
    )


def test_raises_an_error_when_user_is_not_authenticated(graphql_client):
    resp = _get_scan_query(
        graphql_client,
        variables={"id": "1"},
    )

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


def test_works(user, graphql_client):
    conference = ConferenceFactory()

    graphql_client.force_login(user)

    scan = BadgeScan.objects.create(
        scanned_by_id=user.id,
        conference=conference,
        scanned_user_id=UserFactory().id,
        badge_url="https://foo.bar",
        notes="",
    )

    resp = _get_scan_query(
        graphql_client,
        variables={"id": scan.id},
    )

    assert resp["data"]["badgeScan"]["id"] == str(scan.id)


def test_returns_none_when_scan_does_not_exist(user, graphql_client):
    graphql_client.force_login(user)

    resp = _get_scan_query(
        graphql_client,
        variables={"id": "1"},
    )

    assert resp["data"]["badgeScan"] is None


def test_returns_none_when_scan_by_other_user(user, graphql_client):
    conference = ConferenceFactory()

    graphql_client.force_login(user)

    scan = BadgeScan.objects.create(
        scanned_by_id=UserFactory().id,
        conference=conference,
        scanned_user_id=UserFactory().id,
        badge_url="https://foo.bar",
        notes="",
    )

    resp = _get_scan_query(
        graphql_client,
        variables={"id": scan.id},
    )

    assert resp["data"]["badgeScan"] is None
