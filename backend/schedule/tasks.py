from django.db.models import Q
from conferences.tasks import send_conference_voucher_email
from conferences.vouchers import create_conference_voucher
from conferences.models.conference_voucher import ConferenceVoucher
from pycon.celery_utils import OnlyOneAtTimeTask
from google_api.exceptions import NoGoogleCloudQuotaLeftError
from googleapiclient.errors import HttpError
from google_api.sdk import youtube_videos_insert, youtube_videos_set_thumbnail
from integrations import plain
from pretix import user_has_admission_ticket
from django.utils import timezone
from grants.tasks import get_name
from notifications.models import EmailTemplate, EmailTemplateIdentifier
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
from schedule.models import ScheduleItem

logger = logging.getLogger(__name__)


@app.task
def send_schedule_invitation_email(*, schedule_item_id, is_reminder):
    schedule_item = ScheduleItem.objects.get(id=schedule_item_id)
    submission = schedule_item.submission
    language_code = schedule_item.language.code
    conference = schedule_item.conference

    invitation_url = urljoin(
        settings.FRONTEND_URL, f"/schedule/invitation/{submission.hashid}"
    )

    speaker_id = submission.speaker_id
    submission_title = submission.title.localize(language_code)

    speaker = User.objects.get(id=speaker_id)
    conference_name = conference.name.localize("en")

    email_template = EmailTemplate.objects.for_conference(conference).get_by_identifier(
        EmailTemplateIdentifier.proposal_scheduled
    )

    email_template.send_email(
        recipient=speaker,
        placeholders={
            "proposal_title": submission_title,
            "conference_name": conference_name,
            "invitation_url": invitation_url,
            "speaker_name": get_name(speaker, "there"),
            "is_reminder": is_reminder,
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
    proposal_title = submission.title.localize(schedule_item.language.code)

    invitation_url = urljoin(
        settings.FRONTEND_URL, f"/schedule/invitation/{submission.hashid}"
    )

    proposal_speaker = User.objects.get(id=speaker_id)
    conference = schedule_item.conference
    conference_name = schedule_item.conference.name.localize("en")

    email_template = EmailTemplate.objects.for_conference(conference).get_by_identifier(
        EmailTemplateIdentifier.proposal_scheduled_time_changed
    )
    email_template.send_email(
        recipient=proposal_speaker,
        placeholders={
            "proposal_title": proposal_title,
            "invitation_url": invitation_url,
            "conference_name": conference_name,
            "speaker_name": get_name(proposal_speaker, "there"),
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
        oauth_token=conference.get_slack_oauth_token(),
        channel_id=conference.slack_speaker_invitation_answer_channel_id,
    )


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

    email_template = EmailTemplate.objects.for_conference(conference).get_by_identifier(
        EmailTemplateIdentifier.speaker_communication
    )
    email_template.send_email(
        recipient=user,
        placeholders={
            "conference_name": conference.name.localize("en"),
            "user_name": get_name(user, "there"),
            "body": body.replace("\n", "<br />"),
            "subject": subject,
        },
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


def upload_schedule_item_video(*, sent_for_video_upload_state_id: int):
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
        assert video_id, "Video marked as uploaded but Video ID is missing"

        logger.info("Extracting thumbnail for schedule_item_id=%s", schedule_item.id)

        thumbnail_path = extract_video_thumbnail(
            remote_video_path,
            schedule_item.id,
        )

        # we don't need the video file anymore as we already extracted the thumbnail
        cleanup_local_files(schedule_item.id, delete_thumbnail=False)

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


@app.task(base=OnlyOneAtTimeTask)
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

    for sent_for_video_upload_state in statuses.iterator():
        try:
            upload_schedule_item_video(
                sent_for_video_upload_state_id=sent_for_video_upload_state.id
            )
        except NoGoogleCloudQuotaLeftError:
            logger.info(
                "No google cloud quota left to upload the schedule item %s. Moving back to pending and stopping processing.",
                sent_for_video_upload_state.schedule_item.id,
            )
            sent_for_video_upload_state.status = (
                ScheduleItemSentForVideoUpload.Status.pending
            )
            sent_for_video_upload_state.failed_reason = "No Google Cloud Quota Left"
            sent_for_video_upload_state.save(update_fields=["status", "failed_reason"])
            break
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


@app.task
def create_and_send_voucher_to_speaker(schedule_item_id: int):
    schedule_item = ScheduleItem.objects.get(id=schedule_item_id)
    speakers = schedule_item.speakers

    if not speakers:
        return

    speaker = speakers[0]
    co_speaker = speakers[1] if len(speakers) > 1 else None

    _send_conference_voucher(
        speaker,
        schedule_item.conference,
        ConferenceVoucher.VoucherType.SPEAKER,
    )

    if co_speaker:
        _send_conference_voucher(
            co_speaker,
            schedule_item.conference,
            ConferenceVoucher.VoucherType.CO_SPEAKER,
        )


def _send_conference_voucher(user, conference, voucher_type):
    conference_voucher = (
        ConferenceVoucher.objects.for_conference(conference).for_user(user).first()
    )

    if conference_voucher:
        logger.info(
            "User %s already has a voucher for conference %s, not creating a new one",
            user.id,
            conference.id,
        )
        return

    conference_voucher = create_conference_voucher(
        conference=conference,
        user=user,
        voucher_type=voucher_type,
    )

    send_conference_voucher_email.delay(conference_voucher_id=conference_voucher.id)
