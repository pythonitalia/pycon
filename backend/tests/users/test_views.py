import pytest
from django.urls import reverse
from users.models import User


def test_post_login_view(client):
    url = reverse("post-login")
    response = client.get(url)

    assert response.status_code == 200

    assert b"Something went wrong." in response.content


@pytest.mark.django_db
def test_post_login_view_as_logged(client):
    user = User.objects.create_user("lennon@thebeatles.com", "johnpassword")

    client.login(username="lennon@thebeatles.com", password="johnpassword")

    url = reverse("post-login")
    response = client.get(url)

    assert response.status_code == 200

    assert b"lennon@thebeatles.com" in response.content
