import logging
from datetime import datetime, timezone
from decimal import Decimal

from dateutil import parser
from dateutil.relativedelta import relativedelta
from pythonit_toolkit.service_client import ServiceClient

from src.association.settings import SERVICE_TO_SERVICE_SECRET, USERS_SERVICE_URL
from src.association_membership.domain.entities import PaymentStatus, PretixPayment
from src.association_membership.domain.repository import AssociationMembershipRepository
from src.webhooks.exceptions import (
    NoConfirmedPaymentFound,
    NotEnoughPaid,
    NoUserFoundWithEmail,
    UnsupportedMultipleMembershipInOneOrder,
    UserIsAlreadyAMember,
)

from .api import PretixAPI

logger = logging.getLogger(__file__)

GET_USER_ID_BY_EMAIL = """query UserIdByEmail($email: String!) {
    userByEmail(email: $email) {
        id
    }
}"""


async def pretix_event_order_paid(payload):
    action = payload["action"]
    organizer = payload["organizer"]
    event = payload["event"]
    order_code = payload["code"]

    pretix_api = PretixAPI(organizer, event)

    order_data = pretix_api.get_order_data(order_code)

    invalid_order_statuses = ["n", "e", "c"]
    order_status = order_data["status"]
    if order_status in invalid_order_statuses:
        logger.error(
            "Received a paid order event for order_code=%s but the order_status=%s "
            "we only want paid orders",
            order_code,
            order_status,
        )
        return

    categories = pretix_api.get_categories()["results"]
    association_category = next(
        (
            category
            for category in categories
            if category["internal_name"] == "Association"
        ),
        None,
    )

    if not association_category:
        logger.info(
            "Ignoring order_code=%s paid event for organizer=%s event=%s "
            "because there isn't an association category",
            order_code,
            organizer,
            event,
        )
        return

    valid_items = pretix_api.get_items(
        qs={"category": association_category["id"], "active": "true"}
    )
    valid_items_ids = [item["id"] for item in valid_items["results"]]

    order_positions = order_data["positions"]
    membership_positions = []
    for position in order_positions:
        if position["item"] in valid_items_ids:
            membership_positions.append(position)

    if not membership_positions:
        logger.info(
            "No membership positions for order_code=%s so nothing to do", order_code
        )
        return

    if len(membership_positions) > 1:
        logger.error(
            "Multiple positions found in order_code=%s (organizer=%s event=%s) that subscribe "
            "the user to the association. "
            "This is not supported and needs to be refunded or manually handled",
            order_code,
            organizer,
            event,
        )
        raise UnsupportedMultipleMembershipInOneOrder(
            f"Multiple positions found in order_code={order_code} that subscribe the user to the association. This is not supported."
        )

    user_email = order_data["email"]
    client = ServiceClient(
        url=f"{USERS_SERVICE_URL}/internal-api",
        service_name="users-backend",
        caller="association-backend",
        jwt_secret=str(SERVICE_TO_SERVICE_SECRET),
    )
    result = await client.execute(GET_USER_ID_BY_EMAIL, {"email": user_email})
    data = result.data

    if not data["userByEmail"]:
        raise NoUserFoundWithEmail(
            f"No user found with the email of order_code={order_code}"
        )

    user_id = int(data["userByEmail"]["id"])
    repository = AssociationMembershipRepository()

    idempotency_key = PretixPayment.generate_idempotency_key(
        organizer, event, order_code
    )
    if await repository.is_payment_already_processed(idempotency_key):
        logger.info(
            "Ignoring action=%s (organizer=%s event=%s) from Pretix because we already processed "
            "the payment with key=%s from order_code=%s",
            action,
            organizer,
            event,
            idempotency_key,
            order_code,
        )
        return

    subscription = await repository.get_user_subscription(user_id)

    if not subscription:
        subscription = await repository.create_subscription(user_id)

    if subscription.is_active:
        logger.error(
            "user_id=%s is already subscribed to the association "
            "but paid a subscription via order_code=%s (organizer=%s event=%s)!",
            user_id,
            order_code,
            organizer,
            event,
        )
        raise UserIsAlreadyAMember("User is already subscribed to the association")

    membership_position = membership_positions[0]
    membership_price = Decimal(membership_position["price"])
    paid_payments = [
        payment for payment in order_data["payments"] if payment["state"] == "confirmed"
    ]

    if not paid_payments:
        logger.error(
            "user_id=%s is already subscribed to the association "
            "but paid a subscription via order_code=%s (organizer=%s event=%s)!",
            user_id,
            order_code,
            organizer,
            event,
        )
        raise NoConfirmedPaymentFound(
            f"No confirmed payment found for order_code={order_code}"
        )

    total_refunded = sum(
        [
            Decimal(refund["amount"])
            for refund in order_data["refunds"]
            if refund["state"] == "done"
        ]
    )
    total_paid = sum([Decimal(payment["amount"]) for payment in paid_payments])

    if (total_paid - total_refunded) < membership_price:
        logger.error(
            "Received event paid for order_code=%s (organizer=%s event=%s) "
            "but the total_paid=%s (total_refunded=%s) doesn't cover the membership_price=%s "
            " so the membership cannot be created.",
            order_code,
            organizer,
            event,
            total_paid,
            total_refunded,
            membership_price,
        )
        raise NotEnoughPaid(
            f"Not enough payments found for order_code={order_code} to cover total={membership_price}"
        )

    payment_date = next(
        (
            payment["payment_date"]
            for payment in paid_payments
            if payment["payment_date"]
        ),
        None,
    )
    if not payment_date:
        raise ValueError(f"No payment date for order_code={order_code}")

    payment_date = parser.parse(payment_date)
    period_start = payment_date
    period_end = payment_date + relativedelta(years=+1)

    # We assume our currency is EUR that has 2 decimal places and works in cents
    total = int(membership_price * 10 ** 2)
    logger.info(
        "Adding new pretix payment to user_id=%s "
        "for period_start=%s to period_end=%s for order_code=%s organizer=%s event=%s",
        user_id,
        period_start,
        period_end,
        order_code,
        organizer,
        event,
    )
    subscription.add_pretix_payment(
        organizer=organizer,
        event=event,
        order_code=order_code,
        total=total,
        status=PaymentStatus.PAID,
        payment_date=payment_date,
        period_start=period_start,
        period_end=period_end,
    )

    # If the payment we just received is for the current
    # period, we mark the subscription as active
    now = datetime.now(timezone.utc)
    if period_start <= now <= period_end:
        subscription.mark_as_active()

    await repository.save_subscription(subscription)
