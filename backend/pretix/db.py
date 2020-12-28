import json
from typing import List, Optional

from api.pretix.types import Voucher
from conferences.models import Conference
from django.conf import settings
from django.db import connections
from pretix import UpdateTicketInput, get_questions


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
        # items = get_items(conference)

        item_id = found_item[0]

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
