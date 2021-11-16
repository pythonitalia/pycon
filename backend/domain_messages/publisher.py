import json

import boto3
from django.conf import settings


def sqs_message(func):
    if not settings.SQS_QUEUE_URL:

        def noop(*args, **kwargs):
            pass

        return noop
    return func


@sqs_message
def notify_new_submission(
    submission_id: int,
    title: str,
    elevator_pitch: str,
    submission_type: str,
    admin_url: str,
    duration: str,
    topic: str,
):
    sqs = boto3.resource("sqs")
    queue = sqs.Queue(settings.SQS_QUEUE_URL)
    body = json.dumps(
        {
            "title": title,
            "elevator_pitch": elevator_pitch,
            "submission_type": submission_type,
            "admin_url": admin_url,
            "topic": topic,
            "duration": duration,
        }
    )
    queue.send_message(
        MessageBody=body,
        MessageAttributes={"MessageType": {"StringValue": "NewCFPSubmission"}},
        MessageDeduplicationId=submission_id,
    )
