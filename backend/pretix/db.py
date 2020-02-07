from typing import List

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
