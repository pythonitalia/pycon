def test_dashboard_renders_inertia_page(client):
    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "X-Inertia" in response.headers["Vary"]
    assert b'"component": "Dashboard"' in response.content


def test_dashboard_supports_inertia_requests(client):
    response = client.get("/dashboard", headers={"X-Inertia": "true"})

    assert response.status_code == 200
    assert response.headers["X-Inertia"] == "true"
    assert response.json()["component"] == "Dashboard"
