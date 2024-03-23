import pytest
from django.urls import reverse
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_healthcheck_view(client, settings):
    settings.GITHASH = "testversion"
    UserFactory()

    response = client.get(reverse("healthcheck"))
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "testversion"}
