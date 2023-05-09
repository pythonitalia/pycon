from badge_scanner.models import BadgeScan

import pytest

pytestmark = pytest.mark.django_db

def _scan_badge_mutation(graphql_client, variables):
    return graphql_client.query(
        """
        mutation ScanBadge($url: String!, $conferenceCode: String!) {
            scanBadge(input: { url: $url, conferenceCode: $conferenceCode }) {
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


def test_raises_an_error_when_user_is_not_authenticated(graphql_client, conference):
    resp = _scan_badge_mutation(
        graphql_client,
        variables={"url": "https://foo.bar", "conferenceCode": conference.code},
    )

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


# TODO: make sure the user is a sponsor


def test_works_when_user_is_logged_in(user, graphql_client, conference, mocker):
    graphql_client.force_login(user)

    mocker.patch(
        "api.badge_scanner.schema.pretix.get_order_position",
        return_value={
            "attendee_name": "Test User",
            "attendee_email": "barko@marco.pizza",
        },
    )

    mocker.patch(
        "api.badge_scanner.schema.get_user_by_email",
        return_value={
            "id": 1,
            "email": "barko@marco.pizza",
            "full_name": "Test User",
        },
    )

    resp = _scan_badge_mutation(
        graphql_client,
        variables={
            "url": "https://pycon.it/b/this-is-a-test",
            "conferenceCode": conference.code,
        },
    )

    assert "errors" not in resp
    assert resp["data"]["scanBadge"]["__typename"] == "BadgeScan"
    assert resp["data"]["scanBadge"]["attendee"]["fullName"] == "Test User"
    assert resp["data"]["scanBadge"]["attendee"]["email"] == "barko@marco.pizza"
    assert resp["data"]["scanBadge"]["notes"] == ""

    badge_scan = BadgeScan.objects.get()

    assert badge_scan.scanned_by_id == user.id
    assert badge_scan.scanned_user_id == 1
    assert badge_scan.notes == ""
    assert badge_scan.conference == conference
    assert badge_scan.badge_url == "https://pycon.it/b/this-is-a-test"


def test_fails_when_conference_is_wrong(user, graphql_client):
    graphql_client.force_login(user)

    resp = _scan_badge_mutation(
        graphql_client,
        variables={
            "url": "https://clearly-wrong-url.com",
            "conferenceCode": "pycon2023",
        },
    )

    assert "errors" not in resp
    assert resp["data"]["scanBadge"]["__typename"] == "ScanError"
    assert resp["data"]["scanBadge"]["message"] == "Conference not found"


def test_when_url_is_wrong(user, graphql_client, conference):
    graphql_client.force_login(user)

    resp = _scan_badge_mutation(
        graphql_client,
        variables={
            "url": "https://clearly-wrong-url.com",
            "conferenceCode": conference.code,
        },
    )

    assert "errors" not in resp
    assert resp["data"]["scanBadge"]["__typename"] == "ScanError"
    assert resp["data"]["scanBadge"]["message"] == "URL is not valid"
