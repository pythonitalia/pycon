import json
from logging import getLogger

import boto3
from django.apps import apps
from django.conf import settings

from domain_events.handler import HANDLERS

logger = getLogger(__name__)


def process_sqs_messages(event):
    apps.populate(settings.INSTALLED_APPS)

    for record in event["Records"]:
        if record["eventSource"] != "aws:sqs":
            logger.info(
                "Skipping message_id=%s because it is not coming from SQS",
                record["messageId"],
            )
            continue

        process_message(record)


def process_message(record):
    message_id = record["messageId"]
    receipt_handle = record["receiptHandle"]

    message_attributes = record["messageAttributes"]
    message_type = message_attributes["MessageType"]["stringValue"]

    handler = HANDLERS.get(message_type, None)

    if not handler:
        logger.info(
            "Received SQS message_id=%s message_type=%s but no handler accepts it",
            message_id,
            message_type,
        )
        return

    data = json.loads(record["body"])
    handler(data)

    sqs = boto3.client("sqs")
    sqs.delete_message(QueueUrl=settings.SQS_QUEUE_URL, ReceiptHandle=receipt_handle)
