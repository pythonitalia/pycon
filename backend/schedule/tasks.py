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
        f"{prefix} Reminder: Your submission was accepted, confirm your presence"
        if is_reminder
        else f"{prefix} Your submission was accepted!"
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
