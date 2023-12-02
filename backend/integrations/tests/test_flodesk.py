import pytest

from integrations.flodesk import SubscriptionResult, subscribe


def test_flodesk_not_configured(settings):
    settings.FLODESK_API_KEY = ""
    with pytest.raises(ValueError, match="Flodesk integration is not configured"):
        subscribe("example@example.org", ip="127.0.0.1")


def test_subscribe_with_not_existent_email(settings, requests_mock):
    settings.FLODESK_API_KEY = "fake"
    settings.FLODESK_SEGMENT_ID = "segment-123"

    email = "example@example.org"

    requests_mock.get(
        f"https://api.flodesk.com/v1/subscribers/{email}",
        status_code=404,
    )
    requests_mock.post(
        "https://api.flodesk.com/v1/subscribers",
        json={"email": email, "status": "active", "segments": []},
    )

    mock_segments = requests_mock.post(
        f"https://api.flodesk.com/v1/subscribers/{email}/segments",
        json={
            "email": email,
            "status": "active",
        },
    )

    resp = subscribe(email, ip="127.0.0.1")

    assert resp == SubscriptionResult.SUBSCRIBED

    payload_sent = mock_segments.last_request.json()
    assert payload_sent == {"segment_ids": [settings.FLODESK_SEGMENT_ID]}


def test_subscribe_with_existent_email_but_not_added_to_segment(
    settings, requests_mock
):
    settings.FLODESK_API_KEY = "fake"
    settings.FLODESK_SEGMENT_ID = "segment-123"

    email = "example@example.org"

    requests_mock.get(
        f"https://api.flodesk.com/v1/subscribers/{email}",
        status_code=200,
        json={
            "status": "active",
            "segments": [{"id": "segment-456", "name": "Segment 456"}],
        },
    )

    mock_segments = requests_mock.post(
        f"https://api.flodesk.com/v1/subscribers/{email}/segments",
        json={
            "email": email,
            "status": "active",
        },
    )

    resp = subscribe(email, ip="127.0.0.1")

    assert resp == SubscriptionResult.SUBSCRIBED

    payload_sent = mock_segments.last_request.json()
    assert payload_sent == {"segment_ids": [settings.FLODESK_SEGMENT_ID]}


def test_subscribe_with_existing_email(settings, requests_mock):
    settings.FLODESK_API_KEY = "fake"
    email = "example@example.org"

    requests_mock.get(
        f"https://api.flodesk.com/v1/subscribers/{email}",
        status_code=200,
        json={
            "status": "active",
            "segments": [{"id": settings.FLODESK_SEGMENT_ID, "name": "Segment 123"}],
        },
    )

    resp = subscribe(email, ip="127.0.0.1")

    assert resp == SubscriptionResult.SUBSCRIBED


@pytest.mark.parametrize("status", ["unsubscribed", "complained"])
def test_subscribe_when_unsubscribed(settings, requests_mock, status):
    settings.FLODESK_API_KEY = "fake"
    email = "example@example.org"

    requests_mock.get(
        f"https://api.flodesk.com/v1/subscribers/{email}",
        status_code=200,
        json={"status": status},
    )

    resp = subscribe(email, ip="127.0.0.1")

    assert resp == SubscriptionResult.OPT_IN_FORM_REQUIRED


def test_bounced_email_is_rejected(settings, requests_mock):
    settings.FLODESK_API_KEY = "fake"
    email = "example@example.org"

    requests_mock.get(
        f"https://api.flodesk.com/v1/subscribers/{email}",
        status_code=200,
        json={"status": "bounced"},
    )

    resp = subscribe(email, ip="127.0.0.1")

    assert resp == SubscriptionResult.UNABLE_TO_SUBSCRIBE


def test_unconfirmed_email(settings, requests_mock):
    settings.FLODESK_API_KEY = "fake"
    email = "example@example.org"

    requests_mock.get(
        f"https://api.flodesk.com/v1/subscribers/{email}",
        status_code=200,
        json={"status": "unconfirmed"},
    )

    resp = subscribe(email, ip="127.0.0.1")

    assert resp == SubscriptionResult.WAITING_CONFIRMATION
