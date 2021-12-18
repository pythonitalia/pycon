import stripe
from starlette.testclient import TestClient
from ward import each, raises, test

from main import app


@test("cannot call pretix webhook without auth")
def _():
    client = TestClient(app)
    response = client.post("/pretix-webhook")
    assert response.status_code == 404


@test("pretix webhook doesn't allow method {method}")
def _(method=each("get", "delete", "patch")):
    client = TestClient(app)
    response = getattr(client, method)("/pretix-webhook")
    assert response.status_code == 405


@test("cannot call pretix webhook with incorrect basic auth")
def _():
    client = TestClient(app)
    response = client.post("/pretix-webhook", auth=("pretix", "secret"))
    assert response.status_code == 400
    assert "Invalid auth" in str(response.content)


@test("can call pretix webhook with correct basic auth")
def _():
    client = TestClient(app)
    response = client.post(
        "/pretix-webhook",
        auth=("pretix", "pretix-webhook-secret"),
        json={"action": "undefined"},
    )
    assert response.status_code == 200


@test("call stripe webhook works without auth")
def _():
    client = TestClient(app)
    with raises(stripe.error.SignatureVerificationError):
        client.post("/stripe-webhook")


@test("call graphql url works without auth")
def _():
    client = TestClient(app)
    response = client.get("/graphql")
    assert response.status_code == 200
