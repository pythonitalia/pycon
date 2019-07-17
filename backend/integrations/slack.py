from logging import getLogger
from typing import List

from django.conf import settings
from requests import post

logger = getLogger(__name__)


class SlackIncomingWebhookError(Exception):
    pass


def send_message(blocks: List[dict], attachments: List[dict]):
    """
    Performs a HTTP post to the Incoming Webhooks slack api.
    Blocks reference: https://api.slack.com/reference/messaging/blocks
    """
    if not settings.SLACK_INCOMING_WEBHOOK_URL:
        logger.info(
            "SLACK_INCOMING_WEBHOOK_URL env variable not set,"
            "skipping slack notification"
        )
        return
    rv = post(
        url=settings.SLACK_INCOMING_WEBHOOK_URL,
        json={"blocks": blocks, "attachments": attachments},
    )
    if rv.status_code != 200:
        raise SlackIncomingWebhookError(rv.text)
