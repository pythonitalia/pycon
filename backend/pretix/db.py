from typing import List, Optional

from api.pretix.types import Voucher
import json

from django.conf import settings
from django.db import connections

from api.pretix.types import UserTicket


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


def get_user_tickets(email: str, event_slug: str):
    if settings.SIMULATE_PRETIX_DB:
        return []

    with connections["pretix"].cursor() as cursor:
        # fetch all the tickets that are assigned to the email
        cursor.execute(
            """
            SELECT
                tPosition.id,
                tItem.id,
                tItem.name,
                tPosition.attendee_name_cached,
                tPosition.attendee_email
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
        """,
            [email, event_slug],
        )

        tickets = cursor.fetchall()

        positions_ids = []

        positions = {}

        for ticket in tickets:
            position_id = ticket[0]
            item_id = ticket[1]

            positions_ids.append(position_id)

            positions[position_id] = {
                "position_id": position_id,
                "item_id": item_id,
                "item_name": json.loads(ticket[2]),
                "attendee_name": ticket[3],
                "attendee_email": ticket[4],
                "answers": [],
            }

        cursor.execute(
            """
            SELECT
                id,
                question_id,
                answer,
                orderposition_id
            FROM pretixbase_questionanswer
            WHERE orderposition_id = ANY(%s)
        """,
            [positions_ids],
        )

        answers = cursor.fetchall()

        for answer in answers:
            answer_id = answer[0]
            position_id = answer[3]

            positions[position_id]["answers"].append(
                {"id": answer_id, "question_id": answer[1], "answer": answer[2]}
            )

        return positions.values()


def get_user_ticket(position_id: str, email: str, event_slug: str):
    if settings.SIMULATE_PRETIX_DB:
        return None

    with connections["pretix"].cursor() as cursor:
        cursor.execute(
            """
            SELECT
                tItem.id,
                tItem.name,
                tPosition.attendee_name_cached,
                tPosition.attendee_email
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
            AND tPosition.id = %s
        """,
            [email, event_slug, position_id],
        )

        if cursor.rowcount < 1:
            return None

        ticket = cursor.fetchone()

        cursor.execute(
            """
            SELECT
                id,
                question_id,
                answer,
                orderposition_id
            FROM pretixbase_questionanswer
            WHERE orderposition_id = %s
        """,
            [position_id],
        )

        answers = cursor.fetchall()

        return {
            "position_id": position_id,
            "item_id": ticket[0],
            "item_name": json.loads(ticket[1]),
            "attendee_name": ticket[2],
            "attendee_email": ticket[3],
            "answers": [
                {"id": answer[0], "question_id": answer[1], "answer": answer[2]}
                for answer in answers
            ],
        }

    return None
