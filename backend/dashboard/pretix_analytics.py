from __future__ import annotations

import logging
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from conferences.models import Conference
from pretix import get_items, get_orders

logger = logging.getLogger(__name__)

CACHE_VERSION = 1
PAID_ORDER_STATUS = "p"
CANCELED_ORDER_STATUS = "c"


def _display_money(value: Decimal) -> str:
    return f"€{value:,.0f}"


def _item_name(item: dict[str, Any]) -> str:
    name = item.get("name")
    if isinstance(name, str):
        return name
    if isinstance(name, dict):
        return str(name.get("en") or name.get("it") or next(iter(name.values()), ""))
    return "Ticket"


def _week_values(today: date) -> list[dict[str, int | str]]:
    current_week = today - timedelta(days=today.weekday())
    return [
        {
            "label": f"{(current_week - timedelta(weeks=offset)).strftime('%b')} "
            f"{(current_week - timedelta(weeks=offset)).day}",
            "value": 0,
        }
        for offset in range(7, -1, -1)
    ]


def unavailable_ticket_analytics(
    conference: Conference,
    *,
    status: str,
) -> dict[str, Any]:
    year = conference.start.year if conference.start else timezone.localdate().year
    return {
        "id": "ticket-sales",
        "title": "Ticket sales",
        "period": "Last 8 weeks",
        "summary": "Pretix data unavailable",
        "total": None,
        "values": _week_values(timezone.localdate(timezone=conference.timezone)),
        "comparisonValues": [],
        "currentLabel": f"{year} cumulative sold",
        "comparisonLabel": f"{year - 1}, same period",
        "annotations": [],
        "comparisonAnnotations": [],
        "breakdown": [],
        "comparisonBreakdown": [],
        "products": [],
        "details": [
            {"label": "Data source", "value": "Pretix"},
            {"label": "Status", "value": status},
        ],
        "allocatedTotal": None,
    }


def _order_datetime(order: dict[str, Any]) -> datetime | None:
    value = parse_datetime(str(order.get("datetime") or ""))
    if value is None:
        return None
    if timezone.is_naive(value):
        return timezone.make_aware(value, timezone=UTC)
    return value


def _build_ticket_analytics(conference: Conference) -> dict[str, Any]:
    items = get_items(conference)
    paid_orders = list(
        get_orders(
            conference,
            {"status": PAID_ORDER_STATUS, "testmode": "false"},
        )
    )
    canceled_orders = list(
        get_orders(
            conference,
            {"status": CANCELED_ORDER_STATUS, "testmode": "false"},
        )
    )

    today = timezone.localdate(timezone=conference.timezone)
    current_week = today - timedelta(days=today.weekday())
    first_week = current_week - timedelta(weeks=7)
    values = _week_values(today)
    counts: Counter[str] = Counter()
    gross = Decimal(0)
    last_seven_days = 0

    for order in paid_orders:
        ordered_at = _order_datetime(order)
        local_order_date = (
            timezone.localtime(ordered_at, timezone=conference.timezone).date()
            if ordered_at
            else None
        )
        admission_positions = []

        for position in order.get("positions", []):
            item_id = str(position.get("item"))
            item = items.get(item_id)
            if not item or not item.get("admission") or position.get("canceled", False):
                continue

            admission_positions.append(position)
            counts[item_id] += 1
            gross += Decimal(str(position.get("price") or "0"))

        if local_order_date is None or not admission_positions:
            continue

        week_index = (local_order_date - first_week).days // 7
        if 0 <= week_index < len(values):
            values[week_index]["value"] += len(admission_positions)
        if local_order_date >= today - timedelta(days=6):
            last_seven_days += len(admission_positions)

    total = sum(counts.values())
    breakdown = []
    products = []
    for item_id, count in sorted(
        counts.items(),
        key=lambda row: (-row[1], _item_name(items[row[0]]).casefold()),
    ):
        item = items[item_id]
        name = _item_name(item)
        price = Decimal(str(item.get("default_price") or "0"))
        breakdown.append(
            {
                "id": item_id,
                "label": f"{name} · {_display_money(price)}",
                "count": count,
                "share": round(count / total * 100) if total else 0,
            }
        )
        products.append(
            {
                "id": item_id,
                "name": name,
                "price": _display_money(price),
                "tier": str(item.get("internal_name") or "Pretix"),
            }
        )

    completed_refunds = sum(
        refund.get("state") == "done"
        for order in [*paid_orders, *canceled_orders]
        for refund in order.get("refunds", [])
    )
    year = conference.start.year if conference.start else today.year

    return {
        "id": "ticket-sales",
        "title": "Ticket sales",
        "period": "Last 8 weeks",
        "summary": f"{_display_money(gross)} gross",
        "total": total,
        "values": values,
        "comparisonValues": [],
        "currentLabel": f"{year} cumulative sold",
        "comparisonLabel": f"{year - 1}, same period",
        "annotations": [],
        "comparisonAnnotations": [],
        "breakdown": breakdown,
        "comparisonBreakdown": [],
        "products": products,
        "details": [
            {"label": "Last 7 days", "value": f"+{last_seven_days:,}"},
            {"label": "Gross", "value": _display_money(gross)},
            {"label": "Refunds processed", "value": f"{completed_refunds:,}"},
        ],
        "allocatedTotal": None,
    }


def load_pretix_ticket_analytics(conference: Conference) -> dict[str, Any]:
    if not settings.PRETIX_API or not settings.PRETIX_API_TOKEN:
        return unavailable_ticket_analytics(conference, status="Not configured")
    if not conference.pretix_organizer_id or not conference.pretix_event_id:
        return unavailable_ticket_analytics(
            conference,
            status="Conference not linked",
        )

    cache_key = (
        f"dashboard:pretix:v{CACHE_VERSION}:"
        f"{conference.pretix_organizer_id}:{conference.pretix_event_id}"
    )
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        analytics = _build_ticket_analytics(conference)
    except (
        InvalidOperation,
        KeyError,
        TypeError,
        ValueError,
        requests.RequestException,
    ):
        logger.exception(
            "Unable to load dashboard ticket analytics from Pretix",
            extra={"conference_code": conference.code},
        )
        analytics = unavailable_ticket_analytics(
            conference,
            status="Temporarily unavailable",
        )
        cache.set(
            cache_key,
            analytics,
            timeout=settings.DASHBOARD_PRETIX_ERROR_CACHE_TIMEOUT,
        )
        return analytics

    cache.set(
        cache_key,
        analytics,
        timeout=settings.DASHBOARD_PRETIX_CACHE_TIMEOUT,
    )
    return analytics
