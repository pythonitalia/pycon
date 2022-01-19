from logging import getLogger
from typing import List

from django.conf import settings
from requests import post

logger = getLogger(__name__)


class SlackIncomingWebhookError(Exception):
    pass


def send_message(blocks: List[dict], attachments: List[dict], *, channel: str):
    if channel == "cfp":
        token = settings.CFP_SLACK_INCOMING_WEBHOOK_URL
    elif channel == "submission-comments":
        token = settings.SUBMISSION_COMMENT_SLACK_INCOMING_WEBHOOK_URL

    """
    Performs a HTTP post to the Incoming Webhooks slack api.
    Blocks reference: https://api.slack.com/reference/messaging/blocks
    """
    if not token:
        logger.info(
            "SLACK_INCOMING_WEBHOOK_URL env variable not set,"
            "skipping slack notification"
        )
        return
    rv = post(
        url=token,
        json={"blocks": blocks, "attachments": attachments},
    )
    if rv.status_code != 200:
        raise SlackIncomingWebhookError(rv.text)
