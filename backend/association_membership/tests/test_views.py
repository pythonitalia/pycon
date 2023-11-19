from django.urls import reverse
import pytest
import stripe
from django.test import override_settings
import time
import hmac
import hashlib

pytestmark = pytest.mark.django_db


def _generate_stripe_signature(payload, secret):
    timestamp = str(int(time.time()))
    signed_payload = f"{timestamp}.{payload}"
    signature = hmac.new(
        secret.encode(), signed_payload.encode(), hashlib.sha256
    ).hexdigest()
    return f"t={timestamp},v1={signature}"


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


@override_settings(STRIPE_WEBHOOK_SECRET="whsec_secret")
def test_call_stripe_webhook__generate_stripe_signature(rest_api_client):
    payload = '{"type": "evt_test_webhook", "object": "event"}'
    secret = "whsec_secret"
    signature = _generate_stripe_signature(payload, secret)

    response = rest_api_client.post(
        reverse("stripe-webhook"),
        data=payload,
        format="json",
        HTTP_STRIPE_SIGNATURE=signature,
    )
    assert response.status_code == 200
