import json
from logging import getLogger
from urllib.parse import urljoin

import boto3
from django.conf import settings

logger = getLogger(__name__)


def publish_message(type: str, body: dict, *, deduplication_id: str):
    if not settings.SQS_QUEUE_URL:
        return

    sqs = boto3.resource("sqs")
    queue = sqs.Queue(settings.SQS_QUEUE_URL)
    json_body = json.dumps(body)

    queue.send_message(
        MessageBody=json_body,
        MessageAttributes={"MessageType": {"StringValue": type, "DataType": "String"}},
        MessageDeduplicationId=f"{type}-{deduplication_id}",
        MessageGroupId=type,
    )


def notify_new_comment_on_submission(
    comment,
    request,
):
    submission = comment.submission
    all_commenters_ids = list(
        submission.comments.distinct().values_list("author_id", flat=True)
    )
    submission_url = urljoin(settings.FRONTEND_URL, f"/submission/{submission.hashid}")
    admin_url = request.build_absolute_uri(comment.get_admin_url())

    publish_message(
        "NewSubmissionComment",
        body={
            "conference_id": comment.submission.conference_id,
            "comment_id": comment.id,
            "speaker_id": comment.submission.speaker_id,
            "submission_title": comment.submission.title.localize("en"),
            "author_id": comment.author_id,
            "comment": comment.text,
            "admin_url": admin_url,
            "all_commenters_ids": all_commenters_ids,
            "submission_url": submission_url,
        },
        deduplication_id=str(comment.id),
    )


def send_volunteers_push_notification(notification_id: int, volunteers_device_id: int):
    publish_message(
        "VolunteersPushNotificationSent",
        body={
            "notification_id": notification_id,
            "volunteers_device_id": volunteers_device_id,
        },
        deduplication_id=f"{notification_id}-{volunteers_device_id}",
    )
