from django.urls import reverse


def test_send_email_only_works_in_post(http_client):
    response = http_client.get(reverse("send_email"))
    assert response.status_code == 403
