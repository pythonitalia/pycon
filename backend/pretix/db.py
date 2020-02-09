from typing import List, Optional

from api.pretix.types import Voucher
from django.conf import settings
from django.db import connections


def user_has_admission_ticket(email: str, event_slug: int):
    if settings.SIMULATE_PRETIX_DB:
        return True

    with connections["pretix"].cursor() as cursor:
        cursor.execute(
            """
            SELECT EXISTS(
                SELECT 1
                FROM pretixbase_orderposition AS tPosition
                LEFT JOIN pretixbase_order AS tOrder
                ON tOrder.id = tPosition.order_id
                LEFT JOIN pretixbase_item AS tItem
                ON tItem.id = tPosition.item_id
                LEFT JOIN pretixbase_event AS tEvent
                ON tEvent.id = tOrder.event_id
                WHERE tPosition.attendee_email = %s
                AND tOrder.status = 'p'
                AND tItem.admission IS TRUE
                AND tEvent.slug = %s
            );
        """,
            [email, event_slug],
        )

        exists = cursor.fetchone()

    return exists[0]


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

    # block_quota and allow_ignore_quota?
    # variation_id? quota_id?
    # id |      code      |      valid_until       | block_quota | allow_ignore_quota | value | event_id | item_id | redeemed | variation_id | quota_id | comment | tag | max_usages |
    # price_mode | subevent_id | show_hidden_items | seat_id

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
                tVoucher.price_mode
            FROM pretixbase_voucher AS tVoucher
            LEFT JOIN pretixbase_event AS tEvent
            ON tEvent.id = tVoucher.event_id
            WHERE tEvent.slug = %s
            AND tVoucher.code = %s
        """,
            [event_slug, code],
        )

        voucher = cursor.fetchone()

        if not voucher:
            return None

        return Voucher(
            id=voucher[0],
            code=voucher[1],
            valid_until=voucher[2],
            value=voucher[3],
            item_id=voucher[4],
            redeemed=voucher[5],
            max_usages=voucher[6],
            price_mode=voucher[7],
        )
