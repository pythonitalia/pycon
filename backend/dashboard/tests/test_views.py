from datetime import timedelta

from django.utils import timezone

from conferences.tests.factories import ConferenceFactory


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
    assert response.json()["props"]["selectedConference"] is None


def test_dashboard_shares_authenticated_user(client, user):
    client.force_login(user)

    response = client.get("/dashboard", headers={"X-Inertia": "true"})

    assert response.json()["props"]["user"] == {
        "name": "Jane Doe",
        "email": "simulated@user.it",
        "avatar": None,
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


def test_dashboard_returns_404_for_unknown_conference(client, user):
    client.force_login(user)

    response = client.get("/dashboard/unknown")

    assert response.status_code == 404


def test_dashboard_login_renders_inertia_page(client):
    response = client.get("/dashboard/login")

    assert response.status_code == 200
    assert "X-Inertia" in response.headers["Vary"]
    assert b'"component": "Login"' in response.content


def test_dashboard_login_supports_inertia_requests(client):
    response = client.get(
        "/dashboard/login?next=/dashboard%3Fsection%3Dprofile",
        headers={"X-Inertia": "true"},
    )

    assert response.status_code == 200
    assert response.headers["X-Inertia"] == "true"
    assert response.json()["component"] == "Login"
    assert response.json()["props"]["nextUrl"] == "/dashboard?section=profile"


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
