from logging import getLogger
from typing import List

from requests import post

logger = getLogger(__name__)


class SlackIncomingWebhookError(Exception):
    pass


def send_message(blocks: List[dict], attachments: List[dict], *, token: str):
    """
    Performs a HTTP post to the Incoming Webhooks slack api.
    Blocks reference: https://api.slack.com/reference/messaging/blocks
    """
    if not token:
        logger.info(
            "Incoming webhook variable is not set," "skipping slack notification"
        )
        return

    response = post(
        url=token,
        json={"blocks": blocks, "attachments": attachments},
    )

    if response.status_code != 200:
        raise SlackIncomingWebhookError(response.text)
