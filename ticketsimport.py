import os
import sqlite3

import requests

pretix_token = os.environ["PRETIX_TOKEN"]

con = sqlite3.connect("p3.db")
con.row_factory = sqlite3.Row


PYCON10_TO_PRETIX_TICKET_ID = {
    # Company early bird
    247: 115,
    # company regular
    250: 116,
    # company on-desk
    253: 118,
    # personal early
    248: 113,
    # personal regular
    251: 114,
    # personal on-desk
    254: 117,
    # student early
    249: 111,
    # student regular
    252: 112,
    # student on-desk
    256: 119,
}

PYCON9_TO_PRETIX_TICKET_ID = {
    # early business
    232: 124,
    # early personal
    233: 122,
    # early student
    234: 120,
    # on-desk business
    238: 127,
    # on-desk personal
    239: 126,
    # regular business
    235: 125,
    # regular personal
    236: 123,
    # regular student
    237: 121,
}

CONFERENCE_CODE = "pycon9"
CODE_PREFIX = "PY9"
TICKETS_MAP = PYCON9_TO_PRETIX_TICKET_ID

cur = con.cursor()
cur.execute(
    """
    SELECT DISTINCT orderitem.order_id AS order_id
    FROM assopy_orderitem AS orderitem
    INNER JOIN conference_ticket AS ticket ON orderitem.ticket_id = ticket.id
    INNER JOIN conference_fare AS fare ON fare.id = ticket.fare_id
    WHERE
        fare.conference = :conference AND
        fare.ticket_type = 'conference'
""",
    {"conference": CONFERENCE_CODE},
)

total_imported = 0
total_failed = 0
total_duplicate = 0

for order_row in cur:
    order_id = int(order_row["order_id"])
    code = f"{CODE_PREFIX}{order_id}"

    order_items_cur = con.cursor()
    order_items_cur.execute(
        """
        SELECT
            ticket.id AS ticket_id,
            fare.id AS fare_id,
            user.email AS user_email,
            ticket.name AS ticket_name,
            ticket.id AS ticket_id,
            user.first_name AS user_first_name,
            user.last_name AS user_last_name,
            assopyorder.created AS order_created,
            p3ticket.assigned_to AS ticket_assigned_to
        FROM assopy_orderitem AS orderitem
        INNER JOIN conference_ticket AS ticket ON orderitem.ticket_id = ticket.id
        INNER JOIN conference_fare AS fare ON fare.id = ticket.fare_id
        INNER JOIN auth_user AS user ON user.id = ticket.user_id
        INNER JOIN assopy_order AS assopyorder ON assopyorder.id = orderitem.order_id
        INNER JOIN p3_ticketconference AS p3ticket ON p3ticket.ticket_id = ticket.id
        WHERE orderitem.order_id = :order_id
    """,
        {"order_id": order_id},
    )

    positions = []
    user_email = None
    order_created = None
    for order_item_row in order_items_cur:
        user_email = order_item_row["user_email"]
        order_created = order_item_row["order_created"]

        attendee_name = (
            order_item_row["ticket_name"]
            or f"{order_item_row['user_first_name']} {order_item_row['user_last_name']}".strip()
        )

        positions.append(
            {
                "item": TICKETS_MAP[order_item_row["fare_id"]],
                "attendee_name": attendee_name,
                "attendee_email": order_item_row["ticket_assigned_to"]
                or order_item_row["user_email"],
            }
        )

    if not positions:
        print(f"Unable to import order {order_id}. No valid order items")
        total_failed = total_failed + 1
        continue

    assert user_email

    response = requests.post(
        f"https://tickets.pycon.it/api/v1/organizers/python-italia/events/{CONFERENCE_CODE}/orders/",
        json={
            "code": code,
            "status": "p",
            "email": user_email,
            "payment_provider": "manual",
            "testmode": "true",
            "created": order_created,
            "payment_date": order_created,
            "send_email": "false",
            "positions": positions,
        },
        headers={"Authorization": f"Token {pretix_token}"},
    )

    if response.status_code == 400:
        data = response.json()
        if "code" in data and data["code"] == ["This order code is already in use."]:
            print(f"Order {code} was already imported")
            total_duplicate = total_duplicate + 1
        else:
            print(f"Failed to import {code}", data)
            total_failed = total_failed + 1
    else:
        total_imported = total_imported + 1


print(
    f"! Import done. Total imported: {total_imported}, "
    f"Total failed: {total_failed}, Total duplicate: {total_duplicate}"
)
