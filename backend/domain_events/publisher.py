import json

import boto3
from django.conf import settings

from submissions.models import SubmissionComment


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


def notify_new_comment_on_submission(
    comment: SubmissionComment,
    request,
):
    admin_url = request.build_absolute_uri(comment.get_admin_url())
    publish_message(
        "NewSubmissionComment",
        body={
            "comment_id": comment.id,
            "speaker_id": comment.submission.speaker_id,
            "submission_title": comment.submission.title,
            "author_id": comment.author_id,
            "comment": comment.text,
            "admin_url": admin_url,
        },
        deduplication_id=str(comment.id),
    )


def notify_new_submission(
    submission_id: int,
    title: str,
    elevator_pitch: str,
    submission_type: str,
    admin_url: str,
    duration: int,
    topic: str,
    speaker_id: int,
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
            "speaker_id": speaker_id,
        },
        deduplication_id=str(submission_id),
    )
