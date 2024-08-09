from django.urls import reverse


def test_wagtail_users_view_is_disabled(client):
    url = reverse("wagtailusers_users:index")
    response = client.get(url)
    assert response.status_code == 200
    assert b"This view is disabled" in response.content
