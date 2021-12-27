import logging
from typing import Any, Callable, Literal, Optional

from src.webhooks.exceptions import WebhookError

from .crons.membership_check_status import membership_check_status
from .pretix.pretix_event_order_paid import pretix_event_order_paid
from .stripe.handle_invoice_paid import handle_invoice_paid

logger = logging.getLogger(__file__)


HANDLERS = {
    "stripe": {
        "invoice.paid": handle_invoice_paid,
    },
    "pretix": {"pretix.event.order.paid": pretix_event_order_paid},
    "crons": {"membership.check_status": membership_check_status},
}


def get_handler(
    service: Literal["stripe", "pretix"], event: str
) -> Optional[Callable[[Any], None]]:
    return HANDLERS.get(service, {}).get(event, None)


async def run_handler(
    service: Literal["stripe", "pretix", "crons"], event_name: str, payload: Any
):
    handler = get_handler(service, event_name)

    if not handler:
        logger.info("No handler found for event=%s and service=%s", event_name, service)
        return None

    logger.info("Running handler for event_name=%s and service=%s", event_name, service)
    try:
        await handler(payload)
    except WebhookError as e:
        logger.exception(
            "Known error while handling event_name=%s and service=%s",
            event_name,
            service,
            exc_info=e,
        )
