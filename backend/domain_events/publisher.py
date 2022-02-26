import json
from urllib.parse import urljoin

import boto3
from django.conf import settings

from schedule.models import ScheduleItem


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
            "comment_id": comment.id,
            "speaker_id": comment.submission.speaker_id,
            "submission_title": comment.submission.title,
            "author_id": comment.author_id,
            "comment": comment.text,
            "admin_url": admin_url,
            "all_commenters_ids": all_commenters_ids,
            "submission_url": submission_url,
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


def send_schedule_invitation_email(schedule_item):
    submission = schedule_item.submission
    invitation_url = urljoin(
        settings.FRONTEND_URL, f"/schedule/invitation/{submission.hashid}"
    )

    publish_message(
        "ScheduleInvitationSent",
        body={
            "speaker_id": submission.speaker_id,
            "submission_title": submission.title,
            "invitation_url": invitation_url,
        },
        deduplication_id=str(schedule_item.id),
    )


def send_new_schedule_invitation_answer(schedule_item, request):
    invitation_admin_url = request.build_absolute_uri(
        schedule_item.get_invitation_admin_url()
    )
    schedule_item_admin_url = request.build_absolute_uri(schedule_item.get_admin_url())
    submission = schedule_item.submission

    publish_message(
        "NewScheduleInvitationAnswer",
        body={
            "speaker_id": submission.speaker_id,
            "submission_title": submission.title,
            "answer": _schedule_item_status_to_message(schedule_item.status),
            "speaker_notes": schedule_item.speaker_invitation_notes,
            "time_slot": str(schedule_item.slot),
            "invitation_admin_url": invitation_admin_url,
            "schedule_item_admin_url": schedule_item_admin_url,
        },
        deduplication_id=str(schedule_item.id),
    )


def _schedule_item_status_to_message(status: str):
    if status == ScheduleItem.STATUS.confirm:
        return "I am happy with the time slot."

    if status == ScheduleItem.STATUS.maybe:
        return "I can make this time slot work if it is not possible to change"

    if status == ScheduleItem.STATUS.rejected:
        return "The time slot does not work for me"

    if status == ScheduleItem.STATUS.cant_attend:
        return "I can't attend the conference anymore"
