from dataclasses import dataclass
from typing import List, Optional

from django.conf import settings
from django.db import connections

from api.pretix.types import Voucher
from pretix import pretix


@dataclass
class Conference:
    pretix_organizer_id: str
    pretix_event_id: str


def user_has_admission_ticket(
    *, email: str, event_organizer: str, event_slug: int
) -> bool:
    response = pretix(
        conference=Conference(
            pretix_organizer_id=event_organizer, pretix_event_id=event_slug
        ),
        endpoint="tickets/attendee-has-ticket",
        method="post",
        json={
            "attendee_email": email,
            # TODO: In the future this method should be changed to send multiple events
            "events": [
                {
                    "organizer_slug": event_organizer,
                    "event_slug": event_slug,
                }
            ],
        },
    )
    response.raise_for_status()
    data = response.json()
    return data["user_has_admission_ticket"]


def get_orders_status(orders: List[str]):
    if settings.SIMULATE_PRETIX_DB:
        return {}

    with connections["pretix"].cursor() as cursor:
        cursor.execute(
            """SELECT code, status FROM pretixbase_order WHERE code = ANY(%s)""",
            [orders],
        )

        statuses = cursor.fetchall()

    return {status[0]: status[1] for status in statuses}


def get_voucher(event_slug: str, code: str) -> Optional[Voucher]:
    if settings.SIMULATE_PRETIX_DB:
        return None

    with connections["pretix"].cursor() as cursor:
        cursor.execute(
            """
            SELECT
                tVoucher.id,
                tVoucher.code,
                tVoucher.valid_until,
                tVoucher.value,
                tVoucher.item_id,
                tVoucher.redeemed,
                tVoucher.max_usages,
                tVoucher.price_mode,
                tVoucher.quota_id,
                tVoucher.variation_id
            FROM pretixbase_voucher AS tVoucher
            LEFT JOIN pretixbase_event AS tEvent
            ON tEvent.id = tVoucher.event_id
            WHERE tEvent.slug = %s
            AND tVoucher.code = %s
            AND tVoucher.redeemed < tVoucher.max_usages
            AND (tVoucher.valid_until IS NULL OR tVoucher.valid_until > NOW())
        """,
            [event_slug, code],
        )

        voucher = cursor.fetchone()

        if not voucher:
            return None

        quota_id = voucher[8]
        item_id = voucher[4]

        all_items = False
        items = []

        if item_id:
            items.append(item_id)
        elif quota_id:
            # the voucher uses quota instead of a item id
            # so we need to fetch the items of the quota

            cursor.execute(
                """
              SELECT item_id
              FROM pretixbase_quota_items
              WHERE quota_id = %s
              """,
                [quota_id],
            )

            quota_items = cursor.fetchall()
            items = [item[0] for item in quota_items]
        else:
            # if no quota is specified and no item id
            # it means we have to select all the items
            all_items = True

        return Voucher(
            id=voucher[0],
            code=voucher[1],
            valid_until=voucher[2],
            value=voucher[3],
            items=items,
            all_items=all_items,
            redeemed=voucher[5],
            max_usages=voucher[6],
            price_mode=voucher[7],
            variation_id=voucher[9],
        )
