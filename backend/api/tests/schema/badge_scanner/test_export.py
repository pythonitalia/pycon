import tablib
from badge_scanner.models import BadgeScan, BadgeScanExport

import pytest

pytestmark = pytest.mark.django_db


def _export_badge_scans_mutation(graphql_client, variables):
    return graphql_client.query(
        """
        mutation ExportBadgeScans($conferenceCode: String!) {
            exportBadgeScans(conferenceCode: $conferenceCode) {
                id
                url
            }
        }
        """,
        variables=variables,
    )


def test_raises_an_error_when_user_is_not_authenticated(graphql_client, conference):
    resp = _export_badge_scans_mutation(
        graphql_client,
        variables={
            "conferenceCode": conference.code,
        },
    )

    assert resp["errors"]
    assert resp["errors"][0]["message"] == "User not logged in"


def test_works_when_user_is_logged_in(user, graphql_client, conference):
    graphql_client.force_login(user)

    badge_scan = BadgeScan.objects.create(
        scanned_by_id=user.id,
        scanned_user_id=1,
        badge_url="https://pycon.it/b/this-is-a-test",
        attendee_email="example@example.com",
        conference=conference,
        notes="",
    )

    BadgeScan.objects.create(
        scanned_by_id=888,
        scanned_user_id=1,
        badge_url="https://pycon.it/b/this-is-a-test",
        attendee_email="another_example@example.com",
        conference=conference,
        notes="",
    )

    resp = _export_badge_scans_mutation(
        graphql_client,
        variables={
            "conferenceCode": conference.code,
        },
    )

    assert "errors" not in resp

    badge_scan_export = BadgeScanExport.objects.get()

    assert resp["data"]["exportBadgeScans"]["id"] == str(badge_scan_export.id)
    assert resp["data"]["exportBadgeScans"]["url"] == badge_scan_export.file.url

    data = tablib.Dataset().load(badge_scan_export.file.read().decode("utf-8"))

    assert data.headers == ["Created", "Attendee Name", "Attendee Email", "Notes"]
    assert data[0] == (
        str(badge_scan.created),
        badge_scan.attendee_name,
        badge_scan.attendee_email,
        badge_scan.notes,
    )

    assert len(data) == 1
