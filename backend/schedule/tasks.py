from django.db.models import Q
from googleapiclient.errors import HttpError
from celery_heimdall import HeimdallTask
from google_api.sdk import youtube_videos_insert, youtube_videos_set_thumbnail
from integrations import plain
from pythonit_toolkit.emails.utils import mark_safe
from pretix import user_has_admission_ticket
from django.utils import timezone
from grants.tasks import get_name
from pythonit_toolkit.emails.templates import EmailTemplate
from notifications.emails import send_email
from urllib.parse import urljoin
from django.conf import settings
import logging
from integrations import slack

from pycon.celery import app
from schedule.models import ScheduleItemSentForVideoUpload
from schedule.video_upload import (
    cleanup_local_files,
    create_video_info,
    download_video_file,
    extract_video_thumbnail,
)
from users.models import User

logger = logging.getLogger(__name__)


@app.task
def send_schedule_invitation_email(*, schedule_item_id, is_reminder):
    from schedule.models import ScheduleItem

    schedule_item = ScheduleItem.objects.get(id=schedule_item_id)
    submission = schedule_item.submission
    language_code = schedule_item.language.code

    invitation_url = urljoin(
        settings.FRONTEND_URL, f"/schedule/invitation/{submission.hashid}"
    )

    speaker_id = submission.speaker_id
    submission_title = submission.title.localize(language_code)

    speaker = User.objects.get(id=speaker_id)
    conference_name = schedule_item.conference.name.localize("en")

    prefix = f"[{conference_name}]"
    subject = (
        f"{prefix} Reminder: Your submission has been accepted, confirm your presence"
        if is_reminder
        else f"{prefix} Your submission has been accepted!"
    )

    send_email(
        template=EmailTemplate.SUBMISSION_ACCEPTED,
        to=speaker.email,
        subject=subject,
        variables={
            "submissionTitle": submission_title,
            "conferenceName": conference_name,
            "firstname": get_name(speaker, "there"),
            "invitationlink": invitation_url,
        },
    )

    schedule_item.speaker_invitation_sent_at = timezone.now()
    schedule_item.save()


@app.task
def send_submission_time_slot_changed_email(*, schedule_item_id):
    from schedule.models import ScheduleItem

    schedule_item = ScheduleItem.objects.get(id=schedule_item_id)
    submission = schedule_item.submission

    speaker_id = submission.speaker_id
    submission_title = submission.title.localize(schedule_item.language.code)

    invitation_url = urljoin(
        settings.FRONTEND_URL, f"/schedule/invitation/{submission.hashid}"
    )

    speaker = User.objects.get(id=speaker_id)
    conference_name = schedule_item.conference.name.localize("en")

    send_email(
        template=EmailTemplate.SUBMISSION_SCHEDULE_TIME_CHANGED,
        to=speaker.email,
        subject=f"[{conference_name}] Your Submission time slot has been changed!",
        variables={
            "submissionTitle": submission_title,
            "firstname": get_name(speaker, "there"),
            "invitationlink": invitation_url,
            "conferenceName": conference_name,
        },
    )


@app.task
def notify_new_schedule_invitation_answer_slack(
    *, schedule_item_id, invitation_admin_url, schedule_item_admin_url
):
    from schedule.models import ScheduleItem

    schedule_item = ScheduleItem.objects.get(id=schedule_item_id)
    conference = schedule_item.conference
    speaker = schedule_item.submission.speaker

    user_name = get_name(speaker)

    speaker_notes = schedule_item.speaker_invitation_notes

    slack.send_message(
        [
            {
                "type": "section",
                "text": {
                    "text": f"{schedule_item.title} - {user_name} answer:",
                    "type": "mrkdwn",
                },
            },
            {
                "type": "section",
                "text": {
                    "text": _schedule_item_status_to_message(schedule_item.status),
                    "type": "mrkdwn",
                },
            },
            {
                "type": "section",
                "text": {
                    "text": f"*Speaker notes*\n{speaker_notes}",
                    "type": "mrkdwn",
                },
            },
        ],
        [
            {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*<{invitation_admin_url}|Open invitation>*",
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*<{schedule_item_admin_url}|Open schedule item>*",
                        },
                    },
                ],
            },
        ],
        token=conference.slack_speaker_invitation_answer_incoming_webhook_url,
    )


@app.task
def send_speaker_voucher_email(speaker_voucher_id):
    from conferences.models import SpeakerVoucher

    speaker_voucher = SpeakerVoucher.objects.get(id=speaker_voucher_id)

    speaker = speaker_voucher.user
    voucher_code = speaker_voucher.voucher_code

    conference_name = speaker_voucher.conference.name.localize("en")

    send_email(
        template=EmailTemplate.SPEAKER_VOUCHER_CODE,
        to=speaker.email,
        subject=f"[{conference_name}] Your Speaker Voucher Code",
        variables={
            "firstname": get_name(speaker, "there"),
            "voucherCode": voucher_code,
            "is_speaker_voucher": speaker_voucher.voucher_type
            == SpeakerVoucher.VoucherType.SPEAKER,
        },
        reply_to=[
            settings.SPEAKERS_EMAIL_ADDRESS,
        ],
    )

    speaker_voucher.voucher_email_sent_at = timezone.now()
    speaker_voucher.save()


@app.task
def send_speaker_communication_email(
    *,
    subject,
    body,
    user_id,
    conference_id,
    only_speakers_without_ticket,
):
    from conferences.models import Conference

    user = User.objects.get(id=user_id)

    conference = Conference.objects.get(id=conference_id)

    if only_speakers_without_ticket and user_has_admission_ticket(
        email=user.email,
        event_organizer=conference.pretix_organizer_id,
        event_slug=conference.pretix_event_id,
    ):
        return

    send_email(
        template=EmailTemplate.SPEAKER_COMMUNICATION,
        to=user.email,
        subject=f"[{conference.name.localize('en')}] {subject}",
        variables={
            "firstname": get_name(user, "there"),
            "body": mark_safe(body.replace("\n", "<br />")),
        },
        reply_to=[
            settings.SPEAKERS_EMAIL_ADDRESS,
        ],
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


@app.task
def send_schedule_invitation_plain_message(*, schedule_item_id, message):
    from schedule.models import ScheduleItem

    if not settings.PLAIN_API:
        return

    schedule_item = ScheduleItem.objects.get(id=schedule_item_id)

    user = schedule_item.submission.speaker
    existing_thread_id = schedule_item.plain_thread_id

    name = get_name(user, "Speaker")
    title = f"{name} Schedule Invitation time slot"
    if existing_thread_id:
        title = "Additional message"

    thread_id = plain.send_message(
        user, title=title, message=message, existing_thread_id=existing_thread_id
    )

    schedule_item.plain_thread_id = thread_id
    schedule_item.save(update_fields=["plain_thread_id"])


@app.task
def upload_schedule_item_video(*, sent_for_video_upload_state_id):
    sent_for_video_upload = ScheduleItemSentForVideoUpload.objects.get(
        id=sent_for_video_upload_state_id
    )

    if not sent_for_video_upload.is_pending:
        logger.info(
            "Schedule Item Sent for upload %s is not pending but %s, skipping",
            sent_for_video_upload_state_id,
            sent_for_video_upload.status,
        )
        return

    sent_for_video_upload.status = ScheduleItemSentForVideoUpload.Status.processing
    sent_for_video_upload.failed_reason = ""
    sent_for_video_upload.attempts += 1
    sent_for_video_upload.last_attempt_at = timezone.now()
    sent_for_video_upload.save(
        update_fields=["status", "attempts", "failed_reason", "last_attempt_at"]
    )

    schedule_item = sent_for_video_upload.schedule_item
    remote_video_path = schedule_item.video_uploaded_path
    video_id = None

    if not sent_for_video_upload.video_uploaded:
        logger.info("Uploading video for schedule_item_id=%s", schedule_item.id)

        video_info = create_video_info(schedule_item)

        logger.info("Downloading video file %s", remote_video_path)

        local_video_path = download_video_file(schedule_item.id, remote_video_path)

        for response in youtube_videos_insert(
            title=video_info.title,
            description=video_info.description,
            tags=video_info.tags_as_str,
            file_path=local_video_path,
        ):
            logger.info(
                "schedule_item_id=%s Video uploading: %s", schedule_item.id, response
            )

        sent_for_video_upload.video_uploaded = True
        sent_for_video_upload.save(update_fields=["video_uploaded"])

        video_id = response["id"]
        schedule_item.youtube_video_id = video_id
        schedule_item.save(update_fields=["youtube_video_id"])
    else:
        logger.info("Video already uploaded for schedule_item_id=%s", schedule_item.id)

    if not sent_for_video_upload.thumbnail_uploaded:
        video_id = video_id or schedule_item.youtube_video_id
        logger.info("Extracting thumbnail for schedule_item_id=%s", schedule_item.id)

        thumbnail_path = extract_video_thumbnail(
            remote_video_path,
            schedule_item.id,
        )

        try:
            youtube_videos_set_thumbnail(
                video_id=video_id,
                thumbnail_path=thumbnail_path,
            )
        except HttpError as e:
            if e.status_code == 429:
                # we reached the daily thumbnail limit
                logger.warning(
                    "Reached the daily thumbnail limit! schedule_item_id=%s moved back to pending",
                    schedule_item.id,
                )
                sent_for_video_upload.status = (
                    ScheduleItemSentForVideoUpload.Status.pending
                )
                sent_for_video_upload.save(update_fields=["status"])
                return

            raise

        sent_for_video_upload.thumbnail_uploaded = True
        sent_for_video_upload.save(update_fields=["thumbnail_uploaded"])

    cleanup_local_files(schedule_item.id)

    logger.info("Video uploaded for schedule_item_id=%s", schedule_item.id)
    sent_for_video_upload.status = ScheduleItemSentForVideoUpload.Status.completed
    sent_for_video_upload.save(update_fields=["status"])


@app.task(
    base=HeimdallTask,
    heimdall={
        "unique": True,
    },
)
def process_schedule_items_videos_to_upload():
    statuses = (
        ScheduleItemSentForVideoUpload.objects.filter(
            Q(last_attempt_at__isnull=True)
            | Q(
                last_attempt_at__lt=timezone.now() - timezone.timedelta(hours=1),
            )
        )
        .to_upload()
        .order_by("last_attempt_at")
    )
    for sent_for_video_upload_state in statuses:
        try:
            upload_schedule_item_video(
                sent_for_video_upload_state_id=sent_for_video_upload_state.id
            )
        except Exception as e:
            logger.exception(
                "Error processing schedule item %s video upload: %s",
                sent_for_video_upload_state.schedule_item.id,
                e,
            )
            sent_for_video_upload_state.status = (
                ScheduleItemSentForVideoUpload.Status.failed
            )
            sent_for_video_upload_state.failed_reason = str(e)
            sent_for_video_upload_state.save(update_fields=["status", "failed_reason"])
