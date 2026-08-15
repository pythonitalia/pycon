def test_dashboard_requires_authentication(client):
    response = client.get("/dashboard")
    inertia_response = client.get("/dashboard", headers={"X-Inertia": "true"})

    assert response.status_code == 302
    assert response.url == "/dashboard/login?next=/dashboard"
    assert inertia_response.status_code == 302
    assert inertia_response.url == "/dashboard/login?next=/dashboard"


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


def test_dashboard_shares_authenticated_user(client, user):
    client.force_login(user)

    response = client.get("/dashboard", headers={"X-Inertia": "true"})

    assert response.json()["props"]["user"] == {
        "name": "Jane Doe",
        "email": "simulated@user.it",
        "avatar": None,
    }


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
