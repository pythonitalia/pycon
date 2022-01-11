import json

import boto3
from django.conf import settings


def publish_message(type: str, body: dict, *, deduplication_id: str):
    if not settings.SQS_QUEUE_URL:
        return

    sqs = boto3.resource("sqs")
    queue = sqs.Queue(settings.SQS_QUEUE_URL)
    json_body = json.dumps(body)

    queue.send_message(
        MessageBody=json_body,
        MessageAttributes={"MessageType": {"StringValue": type, "DataType": "String"}},
        MessageDeduplicationId=deduplication_id,
        MessageGroupId=type,
    )


def notify_new_submission(
    submission_id: int,
    title: str,
    elevator_pitch: str,
    submission_type: str,
    admin_url: str,
    duration: int,
    topic: str,
    author_id: int,
):
    publish_message(
        "NewCFPSubmission",
        {
            "title": title,
            "elevator_pitch": elevator_pitch,
            "submission_type": submission_type,
            "admin_url": admin_url,
            "topic": topic,
            "duration": str(duration),
            "author_id": author_id,
        },
        deduplication_id=str(submission_id),
    )
