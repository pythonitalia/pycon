import json
from hashlib import md5
from logging import getLogger
from urllib.parse import urljoin
from uuid import uuid4

import boto3
from django.conf import settings

from grants.models import Grant

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


def notify_new_submission(
    submission_id: int,
    title: str,
    elevator_pitch: str,
    submission_type: str,
    admin_url: str,
    duration: int,
    topic: str,
    speaker_id: int,
    conference_id: int,
    tags: str,
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
            "conference_id": conference_id,
            "tags": tags,
        },
        deduplication_id=str(submission_id),
    )


def send_schedule_invitation_email(schedule_item, is_reminder: bool = False):
    submission = schedule_item.submission
    language_code = schedule_item.language.code
    invitation_url = urljoin(
        settings.FRONTEND_URL, f"/schedule/invitation/{submission.hashid}"
    )
    event_name = (
        "ScheduleInvitationReminderSent" if is_reminder else "ScheduleInvitationSent"
    )

    publish_message(
        event_name,
        body={
            "speaker_id": submission.speaker_id,
            "submission_title": submission.title.localize(language_code),
            "invitation_url": invitation_url,
            "is_reminder": is_reminder,
        },
        deduplication_id=str(schedule_item.id),
    )


def send_new_schedule_invitation_answer(schedule_item, request):
    invitation_admin_url = request.build_absolute_uri(
        schedule_item.get_invitation_admin_url()
    )
    language_code = schedule_item.language.code

    schedule_item_admin_url = request.build_absolute_uri(schedule_item.get_admin_url())
    submission = schedule_item.submission

    publish_message(
        "NewScheduleInvitationAnswer",
        body={
            "speaker_id": submission.speaker_id,
            "submission_title": submission.title.localize(language_code),
            "answer": _schedule_item_status_to_message(schedule_item.status),
            "speaker_notes": schedule_item.speaker_invitation_notes,
            "time_slot": str(schedule_item.slot),
            "invitation_admin_url": invitation_admin_url,
            "schedule_item_admin_url": schedule_item_admin_url,
        },
        deduplication_id=str(uuid4()),
    )


def _schedule_item_status_to_message(status: str):
    from schedule.models import ScheduleItem

    if status == ScheduleItem.STATUS.confirmed:
        return "I am happy with the time slot."

    if status == ScheduleItem.STATUS.maybe:
        return "I can make this time slot work if it is not possible to change"

    if status == ScheduleItem.STATUS.rejected:
        return "The time slot does not work for me"

    if status == ScheduleItem.STATUS.cant_attend:
        return "I can't attend the conference anymore"

    return "Undefined"


def send_new_submission_time_slot(schedule_item):
    submission = schedule_item.submission
    invitation_url = urljoin(
        settings.FRONTEND_URL, f"/schedule/invitation/{submission.hashid}"
    )

    publish_message(
        "SubmissionTimeSlotChanged",
        body={
            "speaker_id": submission.speaker_id,
            "submission_title": submission.title,
            "invitation_url": invitation_url,
        },
        deduplication_id=str(schedule_item.id),
    )


def send_speaker_voucher_email(speaker_voucher):
    publish_message(
        "SpeakerVoucherEmailSent",
        body={
            "speaker_id": speaker_voucher.user_id,
            "voucher_code": speaker_voucher.voucher_code,
        },
        deduplication_id=str(speaker_voucher.id),
    )


def send_speaker_communication_email(user_id: int, subject: str, body: str):
    deduplication_id = str(md5(f"{user_id}-{subject}".encode("utf-8")).hexdigest())

    publish_message(
        "SpeakerCommunicationSent",
        body={
            "user_id": user_id,
            "subject": subject,
            "body": body,
        },
        deduplication_id=deduplication_id,
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


def send_grant_reply_approved_email(grant: Grant, is_reminder: bool = False):
    logger.info("Sending reply APPROVED email for GRANT %s", grant.id)

    event_name = (
        "GrantReplyApprovedReminderSent" if is_reminder else "GrantReplyApprovedSent"
    )

    logger.info("Sending APPROVED reply email for GRANT %s (publish message)", grant.id)
    return publish_message(
        event_name,
        body={
            "grant_id": grant.id,
            "is_reminder": is_reminder,
        },
        deduplication_id=str(uuid4()),
    )


def send_grant_reply_waiting_list_email(grant: Grant):
    logger.info("Sending reply WAITING_LIST email for GRANT %s", grant.id)

    return publish_message(
        "GrantReplyWaitingListSent",
        body={"grant_id": grant.id},
        deduplication_id=str(grant.id),
    )


def send_grant_reply_rejected_email(grant: Grant):
    logger.info("Publishing GrantReplyRejectedSent for GRANT %s", grant.id)

    return publish_message(
        "GrantReplyRejectedSent",
        body={"grant_id": grant.id},
        deduplication_id=str(grant.id),
    )


def notify_new_grant_reply(grant: Grant, request):
    admin_url = request.build_absolute_uri(grant.get_admin_url())

    return publish_message(
        "NewGrantReply",
        body={"grant_id": grant.id, "admin_url": admin_url},
        deduplication_id=str(uuid4()),
    )


def send_message_to_plain(grant: Grant, message: str):
    publish_message(
        "NewPlainChatSent",
        body={
            "user_id": grant.user_id,
            "message": message,
        },
        deduplication_id=str(uuid4()),
    )
