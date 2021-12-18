import logging
from datetime import datetime, timezone
from decimal import Decimal

from dateutil import parser
from dateutil.relativedelta import relativedelta
from pythonit_toolkit.service_client import ServiceClient

from src.association.settings import SERVICE_TO_SERVICE_SECRET, USERS_SERVICE_URL
from src.association_membership.domain.entities import PaymentStatus, PretixPayment
from src.association_membership.domain.repository import AssociationMembershipRepository
from src.webhooks.exceptions import NoUserFoundWithEmail

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
    categories = {
        result["id"]: result for result in pretix_api.get_categories()["results"]
    }

    order_positions = order_data["positions"]
    membership_positions = []
    for position in order_positions:
        item_data = pretix_api.get_item_data(position["item"])
        category = categories.get(item_data["category"], None)

        assert (
            category
        ), f"order_code={order_code} item={item_data['id']} does not have a valid category={item_data['category']}"

        # Items that are part of a category named "Association"
        # are considerated special items that should subscribe the user to the association
        if category["internal_name"] != "Association":
            continue

        membership_positions.append(position)

    if not membership_positions:
        logger.info(
            "No membership positions for order_code=%s so nothing to do", order_code
        )
        return

    if len(membership_positions) > 1:
        raise ValueError(
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
            "user_id=%s is already subscribed to the association but paid a subscription via order_code=%s!",
            user_id,
            order_code,
        )
        raise ValueError("User is already subscribed to the association")

    membership_position = membership_positions[0]
    paid_payment = next(
        (
            payment
            for payment in order_data["payments"]
            if payment["state"] == "confirmed"
        ),
        None,
    )

    if not paid_payment:
        raise ValueError(f"No confirmed payment found for order_code={order_code}")

    if not paid_payment["payment_date"]:
        raise ValueError(f"No payment date for order_code={order_code}")

    payment_date = parser.parse(paid_payment["payment_date"])
    period_start = payment_date
    period_end = payment_date + relativedelta(years=+1)

    # We assume our currency is EUR that has 2 decimal places and works in cents
    total = int(Decimal(membership_position["price"]) * 10 ** 2)
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
