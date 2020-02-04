import json
from typing import List, Optional

from api.pretix.types import Voucher
import json

from django.conf import settings
from django.db import connections

from conferences.models import Conference

from pretix import get_items, get_questions, UpdateTicketInput

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


def user_owns_order_position(position_id: str, email: str):
    if settings.SIMULATE_PRETIX_DB:
        return None

    with connections["pretix"].cursor() as cursor:
        cursor.execute(
            """
            SELECT EXISTS(
                SELECT 1
                FROM pretixbase_orderposition
                WHERE attendee_email = %s AND id = %s
            )
        """,
            [email, position_id],
        )

        exists = cursor.fetchone()
        return exists[0]


def update_ticket(conference: Conference, position_id: str, input: UpdateTicketInput):
    with connections["pretix"].cursor() as cursor:
        cursor.execute(
            """
        SELECT item_id FROM pretixbase_orderposition WHERE id = %s
        """,
            [position_id],
        )

        found_item = cursor.fetchone()

        if len(found_item) == 0:
            # ??
            raise ValueError("invalid position id?")

        # todo replace with get_item?
        items = get_items(conference)

        item_id = found_item[0]
        item = items[str(item_id)]

        questions = get_questions(conference)
        item_questions = {
            str(question["id"]): question
            for question in questions.values()
            if item_id in question["items"]
        }

        cursor.execute(
            """
        UPDATE pretixbase_orderposition SET attendee_name_parts = %s, attendee_name_cached = %s WHERE id = %s
        """,
            [
                json.dumps({"_scheme": "full", "full_name": input.attendee_name}),
                input.attendee_name,
                position_id,
            ],
        )

        cursor.execute(
            """
        UPDATE pretixbase_orderposition SET attendee_email = %s WHERE id = %s
        """,
            [input.attendee_email, position_id],
        )

        answers = {answer.question_id: answer for answer in input.answers}

        for question_id, question in item_questions.items():
            if question_id not in answers:
                # Question not answered, do nothing with it?
                continue

            answer = answers[question_id].answer
            text_answer = answer

            if question["type"] == "C":
                options = {str(option["id"]): option for option in question["options"]}

                if answer not in options.keys():
                    # Answer ID not valid
                    raise ValueError("answer id not valid")

                text_answer = options[answer]["answer"]["en"]

            if question["required"] and not answer:
                # TODO: Raise error here, how?
                raise ValueError("Empty answer not allowed")

            update_or_insert(
                cursor,
                update_query="UPDATE pretixbase_questionanswer SET answer = %s WHERE orderposition_id = %s AND question_id = %s RETURNING id",
                update_args=[text_answer, position_id, question_id],
                insert_query="INSERT INTO pretixbase_questionanswer (answer, orderposition_id, question_id) VALUES (%s, %s, %s) RETURNING id",
                insert_args=[text_answer, position_id, question_id],
            )

            question_answer_id = cursor.fetchone()[0]

            if question["type"] == "C":
                #  add new row
                update_or_insert(
                    cursor,
                    update_query="UPDATE pretixbase_questionanswer_options SET questionoption_id = %s WHERE questionanswer_id = %s",
                    update_args=[answer, question_answer_id],
                    insert_query="INSERT INTO pretixbase_questionanswer_options (questionanswer_id, questionoption_id) VALUES (%s, %s)",
                    insert_args=[answer, question_answer_id],
                )
    pass


def update_or_insert(cursor, update_query, update_args, insert_query, insert_args):
    cursor.execute(update_query, update_args)

    if cursor.rowcount == 0:
        cursor.execute(insert_query, insert_args)
