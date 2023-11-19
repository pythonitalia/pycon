from django.urls import reverse
import pytest
import stripe
from django.test import override_settings

pytestmark = pytest.mark.django_db


def test_cannot_call_pretix_webhook_without_auth(rest_api_client):
    response = rest_api_client.post(reverse("pretix-webhook"))
    assert response.status_code == 401


@override_settings(PRETIX_WEBHOOK_SECRET="secret")
def test_pretix_webhook_does_not_allow_method(rest_api_client):
    rest_api_client.basic_auth("pretix", "secret")
    for method in ["get", "delete", "patch"]:
        response = getattr(rest_api_client, method)(
            reverse("pretix-webhook"),
        )
        assert response.status_code == 405


@override_settings(PRETIX_WEBHOOK_SECRET="secret")
def test_cannot_call_pretix_webhook_with_incorrect_basic_auth(rest_api_client):
    rest_api_client.basic_auth("pretix", "incorrect")
    response = rest_api_client.post(reverse("pretix-webhook"))

    assert response.status_code == 401
    assert "Incorrect authentication credentials." in response.json()["detail"]


@override_settings(PRETIX_WEBHOOK_SECRET="secret")
def test_can_call_pretix_webhook_with_correct_basic_auth(rest_api_client):
    rest_api_client.basic_auth("pretix", "secret")
    response = rest_api_client.post(
        reverse("pretix-webhook"), data={"action": "undefined"}, format="json"
    )
    assert response.status_code == 200


def test_call_stripe_webhook_doesnt_work_without_auth(rest_api_client):
    with pytest.raises(stripe.error.SignatureVerificationError):
        rest_api_client.post(reverse("stripe-webhook"))
