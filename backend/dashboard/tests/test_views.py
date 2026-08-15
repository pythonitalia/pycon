from datetime import UTC, datetime, timedelta

from django.test import override_settings
from django.utils import timezone

from conferences.models import Deadline
from conferences.tests.factories import ConferenceFactory, DeadlineFactory
from grants.models import Grant
from grants.tests.factories import (
    GrantFactory,
    GrantReimbursementCategoryFactory,
    GrantReimbursementFactory,
)
from i18n.strings import LazyI18nString
from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory


def test_dashboard_requires_authentication(client):
    response = client.get("/dashboard")
    inertia_response = client.get("/dashboard", headers={"X-Inertia": "true"})
    conference_response = client.get("/dashboard/pycon-2026")

    assert response.status_code == 302
    assert response.url == "/dashboard/login?next=/dashboard"
    assert inertia_response.status_code == 302
    assert inertia_response.url == "/dashboard/login?next=/dashboard"
    assert conference_response.status_code == 302
    assert conference_response.url == "/dashboard/login?next=/dashboard/pycon-2026"


@override_settings(DASHBOARD_REQUIRE_STAFF=True)
def test_dashboard_rejects_non_staff_users(client, user):
    client.force_login(user)

    response = client.get("/dashboard")

    assert response.status_code == 403


@override_settings(DASHBOARD_REQUIRE_STAFF=True)
def test_dashboard_allows_staff_users(client, admin_user):
    client.force_login(admin_user)

    response = client.get("/dashboard")

    assert response.status_code == 200


def test_dashboard_renders_inertia_page(client, user):
    client.force_login(user)

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "X-Inertia" in response.headers["Vary"]
    assert b'"component": "Dashboard"' in response.content


def test_dashboard_supports_inertia_requests(client, user):
    client.force_login(user)

    response = client.get("/dashboard", headers={"X-Inertia": "true"})

    assert response.status_code == 200
    assert response.headers["X-Inertia"] == "true"
    assert response.json()["component"] == "Dashboard"
    assert response.json()["props"]["user"]["email"] == "simulated@user.it"
    assert response.json()["props"]["conferences"] == []
    assert response.json()["props"]["maxComparisonConferences"] == 2
    assert response.json()["props"]["comparisonConferences"] == []
    assert response.json()["props"]["selectedConference"] is None


@override_settings(FRONTEND_URL="https://pycon.it")
def test_dashboard_shares_authenticated_user(client, user):
    client.force_login(user)

    response = client.get("/dashboard", headers={"X-Inertia": "true"})

    assert response.json()["props"]["user"] == {
        "name": "Jane Doe",
        "email": "simulated@user.it",
        "avatar": None,
        "profileUrl": "https://pycon.it/profile",
    }


def test_dashboard_redirects_to_latest_conference(client, user):
    client.force_login(user)
    ConferenceFactory(
        code="pycon-2025",
        start=timezone.now() - timedelta(days=365),
    )
    latest_conference = ConferenceFactory(
        code="pycon-2026",
        start=timezone.now(),
    )

    response = client.get("/dashboard")

    assert response.status_code == 302
    assert response.url == f"/dashboard/{latest_conference.code}"


def test_dashboard_uses_conference_from_url(client, user):
    client.force_login(user)
    selected_conference = ConferenceFactory(code="pycon-2025")
    ConferenceFactory(code="pycon-2026")

    response = client.get(
        f"/dashboard/{selected_conference.code}",
        headers={"X-Inertia": "true"},
    )

    assert response.status_code == 200
    assert response.json()["props"]["selectedConference"]["code"] == "pycon-2025"
    assert {
        conference["code"] for conference in response.json()["props"]["conferences"]
    } == {
        "pycon-2025",
        "pycon-2026",
    }


def test_dashboard_uses_comparison_conferences_from_query_string(client, user):
    client.force_login(user)
    selected_conference = ConferenceFactory(code="pycon2026")
    comparison_conference = ConferenceFactory(code="pycon2025")
    ConferenceFactory(code="pycon2024")

    response = client.get(
        (
            f"/dashboard/{selected_conference.code}"
            f"?compare={comparison_conference.code}"
            "&compare=unknown&compare=pycon2026"
        ),
        headers={"X-Inertia": "true"},
    )

    comparisons = response.json()["props"]["comparisonConferences"]
    assert [conference["code"] for conference in comparisons] == ["pycon2025"]
    assert comparisons[0]["analytics"][0]["id"] == "ticket-sales"


@override_settings(DASHBOARD_MAX_COMPARISON_CONFERENCES=1)
def test_dashboard_limits_comparison_conferences(client, user):
    client.force_login(user)
    selected_conference = ConferenceFactory(
        code="pycon2026",
        start=timezone.now(),
    )
    ConferenceFactory(
        code="pycon2025",
        start=timezone.now() - timedelta(days=365),
    )
    ConferenceFactory(
        code="pycon2024",
        start=timezone.now() - timedelta(days=730),
    )

    response = client.get(
        f"/dashboard/{selected_conference.code}?compare=pycon2025&compare=pycon2024",
        headers={"X-Inertia": "true"},
    )

    props = response.json()["props"]
    assert props["maxComparisonConferences"] == 1
    assert [conference["code"] for conference in props["comparisonConferences"]] == [
        "pycon2025"
    ]


def test_dashboard_exposes_conference_timeline(client, user, time_machine):
    time_machine.move_to(datetime(2026, 3, 1, tzinfo=UTC))
    client.force_login(user)
    conference = ConferenceFactory(
        code="pycon2026",
        location="Bologna",
        start=datetime(2026, 5, 27, tzinfo=UTC),
        end=datetime(2026, 5, 30, tzinfo=UTC),
    )
    DeadlineFactory(
        conference=conference,
        type=Deadline.TYPES.cfp,
        start=datetime(2025, 10, 1, tzinfo=UTC),
        end=datetime(2026, 2, 1, tzinfo=UTC),
    )
    DeadlineFactory(
        conference=conference,
        type=Deadline.TYPES.voting,
        start=datetime(2026, 2, 2, tzinfo=UTC),
        end=datetime(2026, 3, 8, tzinfo=UTC),
    )
    DeadlineFactory(
        conference=conference,
        type=Deadline.TYPES.custom,
        name=LazyI18nString("Review deadline"),
        start=datetime(2026, 3, 9, tzinfo=UTC),
        end=datetime(2026, 4, 12, tzinfo=UTC),
    )

    response = client.get(
        f"/dashboard/{conference.code}",
        headers={"X-Inertia": "true"},
    )

    selected_conference = response.json()["props"]["selectedConference"]
    assert selected_conference["location"] == "Bologna"
    assert selected_conference["startDate"] == "2026-05-27"
    assert selected_conference["endDate"] == "2026-05-30"
    assert selected_conference["countdown"] == {
        "label": "days to doors",
        "value": "87",
    }
    assert [milestone["label"] for milestone in selected_conference["milestones"]] == [
        "CFP closed",
        "Voting open",
        "Review deadline",
        "Doors open",
    ]
    assert [milestone["status"] for milestone in selected_conference["milestones"]] == [
        "complete",
        "current",
        "upcoming",
        "upcoming",
    ]
    assert selected_conference["milestones"][1]["relative"] == "In 7 days"


def test_dashboard_exposes_live_analytics(
    client,
    user,
    time_machine,
):
    time_machine.move_to(datetime(2026, 3, 1, tzinfo=UTC))
    client.force_login(user)
    conference = ConferenceFactory(code="pycon2026")
    SubmissionFactory(
        conference=conference,
        created=datetime(2026, 1, 6, tzinfo=UTC),
        status=Submission.STATUS.accepted,
    )
    SubmissionFactory(
        conference=conference,
        created=datetime(2026, 2, 24, tzinfo=UTC),
    )
    SubmissionFactory(
        conference=conference,
        created=datetime(2026, 2, 25, tzinfo=UTC),
    )
    grant = GrantFactory(
        conference=conference,
        created=datetime(2026, 2, 10, tzinfo=UTC),
        status=Grant.Status.approved,
    )
    reimbursement_category = GrantReimbursementCategoryFactory(
        conference=conference,
        travel=True,
    )
    GrantReimbursementFactory(
        category=reimbursement_category,
        grant=grant,
        granted_amount=500,
    )

    response = client.get(
        f"/dashboard/{conference.code}",
        headers={"X-Inertia": "true"},
    )

    analytics = response.json()["props"]["selectedConference"]["analytics"]
    assert [chart["title"] for chart in analytics] == [
        "Ticket sales",
        "Proposals received",
        "Grants received",
    ]
    assert analytics[0]["total"] is None
    assert analytics[0]["summary"] == "Pretix data unavailable"
    assert analytics[0]["breakdown"] == []
    assert analytics[0]["details"] == [
        {"label": "Data source", "value": "Pretix"},
        {"label": "Status", "value": "Not configured"},
    ]
    assert analytics[0]["allocatedTotal"] is None
    assert [week["value"] for week in analytics[1]["values"]] == [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        2,
    ]
    assert analytics[1]["total"] == 3
    assert analytics[1]["summary"] == "submitted · all time"
    assert analytics[1]["breakdown"] == [
        {
            "id": "proposed",
            "label": "Awaiting review",
            "count": 2,
            "share": 67,
        },
        {
            "id": "accepted",
            "label": "Accepted",
            "count": 1,
            "share": 33,
        },
    ]
    assert analytics[2]["total"] == 1
    assert analytics[2]["period"] == "All time"
    assert analytics[2]["breakdown"] == [
        {
            "id": "approved",
            "label": "Approved",
            "count": 1,
            "share": 100,
        }
    ]
    assert analytics[2]["allocatedTotal"] == 500


def test_dashboard_returns_404_for_unknown_conference(client, user):
    client.force_login(user)

    response = client.get("/dashboard/unknown")

    assert response.status_code == 404


def test_dashboard_login_renders_inertia_page(client):
    response = client.get("/dashboard/login")

    assert response.status_code == 200
    assert "X-Inertia" in response.headers["Vary"]
    assert b'"component": "Login"' in response.content


@override_settings(FRONTEND_URL="https://pycon.it")
def test_dashboard_login_supports_inertia_requests(client):
    response = client.get(
        "/dashboard/login?next=/dashboard%3Fsection%3Dprofile",
        headers={"X-Inertia": "true"},
    )

    assert response.status_code == 200
    assert response.headers["X-Inertia"] == "true"
    assert response.json()["component"] == "Login"
    assert response.json()["props"] == {
        "nextUrl": "/dashboard?section=profile",
        "privacyPolicyUrl": "https://pycon.it/privacy-policy",
        "resetPasswordUrl": "https://pycon.it/reset-password",
    }


def test_dashboard_login_rejects_external_next_url(client):
    response = client.get(
        "/dashboard/login?next=https://example.com",
        headers={"X-Inertia": "true"},
    )

    assert response.status_code == 200
    assert response.json()["props"]["nextUrl"] == "/dashboard"


def test_dashboard_login_redirects_authenticated_user(client, user):
    client.force_login(user)

    response = client.get("/dashboard/login?next=/dashboard%3Fsection%3Dprofile")

    assert response.status_code == 302
    assert response.url == "/dashboard?section=profile"
