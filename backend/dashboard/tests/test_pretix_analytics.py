from datetime import UTC, datetime

import requests
from django.core.cache import cache
from django.test import override_settings

from conferences.tests.factories import ConferenceFactory
from dashboard import pretix_analytics


@override_settings(
    PRETIX_API="https://pretix.example/api/v1/",
    PRETIX_API_TOKEN="read-only-token",
)
def test_loads_aggregate_ticket_analytics_without_exposing_order_data(
    db,
    monkeypatch,
    time_machine,
):
    time_machine.move_to(datetime(2026, 8, 8, 12, tzinfo=UTC))
    conference = ConferenceFactory(
        code="pycon2026",
        pretix_organizer_id="pycon-italia",
        pretix_event_id="pycon2026",
        start=datetime(2026, 5, 27, tzinfo=UTC),
    )
    items = {
        "1": {
            "admission": True,
            "default_price": "80.00",
            "internal_name": "Student",
            "name": {"en": "Student ticket"},
        },
        "2": {
            "admission": True,
            "default_price": "120.00",
            "internal_name": "Personal",
            "name": {"en": "Personal ticket"},
        },
        "3": {
            "admission": False,
            "default_price": "20.00",
            "internal_name": "T-shirt",
            "name": {"en": "T-shirt"},
        },
    }
    paid_orders = [
        {
            "code": "SECRET1",
            "datetime": "2026-08-05T10:00:00Z",
            "email": "not-returned@example.com",
            "positions": [
                {"item": 1, "price": "80.00"},
                {"item": 1, "price": "80.00"},
                {"item": 3, "price": "20.00"},
            ],
            "refunds": [
                {"state": "done"},
                {"state": "created"},
            ],
        },
        {
            "code": "SECRET2",
            "datetime": "2026-06-16T10:00:00Z",
            "positions": [{"item": 2, "price": "120.00"}],
            "refunds": [],
        },
    ]
    canceled_orders = [
        {
            "code": "SECRET3",
            "datetime": "2026-07-01T10:00:00Z",
            "positions": [],
            "refunds": [{"state": "done"}],
        }
    ]
    order_calls = []

    monkeypatch.setattr(pretix_analytics, "get_items", lambda _conference: items)

    def get_orders(_conference, params):
        order_calls.append(params)
        return paid_orders if params["status"] == "p" else canceled_orders

    monkeypatch.setattr(pretix_analytics, "get_orders", get_orders)

    analytics = pretix_analytics.load_pretix_ticket_analytics(conference)

    assert analytics["total"] == 3
    assert analytics["summary"] == "€280 gross"
    assert [week["value"] for week in analytics["values"]] == [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        2,
    ]
    assert analytics["breakdown"] == [
        {
            "id": "1",
            "label": "Student ticket · €80",
            "count": 2,
            "share": 67,
        },
        {
            "id": "2",
            "label": "Personal ticket · €120",
            "count": 1,
            "share": 33,
        },
    ]
    assert analytics["details"] == [
        {"label": "Last 7 days", "value": "+2"},
        {"label": "Gross", "value": "€280"},
        {"label": "Refunds processed", "value": "2"},
    ]
    assert "SECRET1" not in str(analytics)
    assert "not-returned@example.com" not in str(analytics)
    assert order_calls == [
        {"status": "p", "testmode": "false"},
        {"status": "c", "testmode": "false"},
    ]


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "dashboard-pretix-failure-test",
        }
    },
    PRETIX_API="https://pretix.example/api/v1/",
    PRETIX_API_TOKEN="read-only-token",
)
def test_pretix_failure_returns_safe_unavailable_state(db, monkeypatch):
    conference = ConferenceFactory(
        pretix_organizer_id="pycon-italia",
        pretix_event_id="pycon2026",
    )

    cache.clear()
    attempts = 0

    def fail(_conference):
        nonlocal attempts
        attempts += 1
        raise requests.Timeout

    monkeypatch.setattr(pretix_analytics, "get_items", fail)

    analytics = pretix_analytics.load_pretix_ticket_analytics(conference)
    cached_analytics = pretix_analytics.load_pretix_ticket_analytics(conference)

    assert attempts == 1
    assert cached_analytics == analytics
    assert analytics["total"] is None
    assert analytics["details"] == [
        {"label": "Data source", "value": "Pretix"},
        {"label": "Status", "value": "Temporarily unavailable"},
    ]


@override_settings(PRETIX_API="")
def test_missing_pretix_configuration_does_not_make_an_api_request(
    db,
    monkeypatch,
):
    conference = ConferenceFactory()

    def unexpected_call(_conference):
        raise AssertionError("Pretix should not be called")

    monkeypatch.setattr(pretix_analytics, "get_items", unexpected_call)

    analytics = pretix_analytics.load_pretix_ticket_analytics(conference)

    assert analytics["total"] is None
    assert analytics["details"][-1] == {
        "label": "Status",
        "value": "Not configured",
    }
