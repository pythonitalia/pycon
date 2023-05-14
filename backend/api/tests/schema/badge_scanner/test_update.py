from badge_scanner.models import BadgeScan

import pytest

pytestmark = pytest.mark.django_db


def _update_notes_mutation(graphql_client, variables):
    return graphql_client.query(
        """
        mutation UpdateBadgeScan($input: UpdateBadgeScanInput!) {
            updateBadgeScan(input: $input) {
                __typename
                ... on BadgeScan {
                    id
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


def test_raises_an_error_when_user_is_not_authenticated(graphql_client, conference):
    resp = _update_notes_mutation(
        graphql_client,
        variables={
            "input": {
                "id": "1",
                "notes": "This is a test",
            },
        },
    )

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


# TODO: make sure the user is a sponsor


def test_works_when_user_is_logged_in(user, graphql_client, conference):
    graphql_client.force_login(user)

    badge_scan = BadgeScan.objects.create(
        scanned_by_id=user.id,
        scanned_user_id=1,
        badge_url="https://pycon.it/b/this-is-a-test",
        conference=conference,
        notes="",
    )

    resp = _update_notes_mutation(
        graphql_client,
        variables={
            "input": {
                "id": str(badge_scan.id),
                "notes": "This is a test",
            },
        },
    )

    assert "errors" not in resp

    assert resp["data"]["updateBadgeScan"]["__typename"] == "BadgeScan"
    assert resp["data"]["updateBadgeScan"]["notes"] == "This is a test"
    assert resp["data"]["updateBadgeScan"]["id"] == str(badge_scan.id)

    badge_scan.refresh_from_db()

    assert badge_scan.notes == "This is a test"


def test_fails_when_not_their_scan(user, user_factory, conference, graphql_client):
    graphql_client.force_login(user)
    other_user = user_factory()

    badge_scan = BadgeScan.objects.create(
        scanned_by_id=other_user.id,
        scanned_user_id=1,
        badge_url="https://pycon.it/b/this-is-a-test",
        conference=conference,
        notes="",
    )

    resp = _update_notes_mutation(
        graphql_client,
        variables={
            "input": {
                "id": str(badge_scan.id),
                "notes": "This is a test",
            },
        },
    )

    assert "errors" not in resp

    assert resp["data"]["updateBadgeScan"]["__typename"] == "ScanError"
    assert resp["data"]["updateBadgeScan"]["message"] == "Badge scan not found"
