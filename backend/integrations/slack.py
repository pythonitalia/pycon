from logging import getLogger
from typing import List

from requests import post

logger = getLogger(__name__)


class SlackIncomingWebhookError(Exception):
    pass


def send_message(
    blocks: List[dict],
    attachments: List[dict],
    text: str = "",
    *,
    oauth_token: str,
    channel_id: str,
):
    """
    Performs a HTTP post to the Incoming Webhooks slack api.
    Blocks reference: https://api.slack.com/reference/messaging/blocks
    """
    if not oauth_token:
        logger.info("No oauth token provided for sending a slack message.")
        return

    if not channel_id:
        logger.info("No channel ID provided for sending a slack message.")
        return

    response = post(
        url="https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {oauth_token}",
        },
        json={
            "blocks": blocks,
            "attachments": attachments,
            "text": text,
            "channel": channel_id,
        },
    )
    response.raise_for_status()

    payload = response.json()

    if not payload["ok"]:
        raise SlackIncomingWebhookError(payload["error"])
