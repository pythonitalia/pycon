import json
import logging
from pretix import user_has_admission_ticket

import boto3
from django.conf import settings
from django.utils import timezone
from pythonit_toolkit.emails.templates import EmailTemplate
from pythonit_toolkit.emails.utils import mark_safe

from users.models import User
from integrations import slack
from notifications.emails import send_email

logger = logging.getLogger(__name__)


def get_name(user: User, fallback: str = "<no name specified>"):
    return user.full_name or user.name or user.username or fallback


def handle_new_cfp_submission(data):
    from conferences.models import Conference

    title = data["title"]
    elevator_pitch = data["elevator_pitch"]
    submission_type = data["submission_type"]
    admin_url = data["admin_url"]
    tags = data["tags"]
    speaker_id = data["speaker_id"]

    speaker = User.objects.get(id=speaker_id)
    conference = Conference.objects.get(id=data["conference_id"])

    user_name = get_name(speaker)

    slack.send_message(
        [
            {
                "type": "section",
                "text": {
                    "text": f"New _{submission_type}_ proposal by {user_name}",
                    "type": "mrkdwn",
                },
            }
        ],
        [
            {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*<{admin_url}|{title.capitalize()}>*\n"
                            f"*Elevator Pitch*\n{elevator_pitch}",
                        },
                        "fields": [
                            {"type": "mrkdwn", "text": "*Tags*"},
                            {"type": "plain_text", "text": str(tags)},
                        ],
                    }
                ]
            }
        ],
        token=conference.slack_new_proposal_incoming_webhook_url,
    )


def handle_schedule_invitation_sent(data):
    speaker_id = data["speaker_id"]
    invitation_url = data["invitation_url"]
    submission_title = data["submission_title"]
    is_reminder = data.get("is_reminder", False)

    speaker = User.objects.get(id=speaker_id)

    prefix = "[PyCon Italia 2023]"
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
            "firstname": get_name(speaker, "there"),
            "invitationlink": invitation_url,
        },
    )


def handle_submission_time_slot_changed(data):
    speaker_id = data["speaker_id"]
    invitation_url = data["invitation_url"]
    submission_title = data["submission_title"]

    speaker = User.objects.get(id=speaker_id)

    send_email(
        template=EmailTemplate.SUBMISSION_SCHEDULE_TIME_CHANGED,
        to=speaker.email,
        subject="[PyCon Italia 2023] Your Submission time slot has been changed!",
        variables={
            "submissionTitle": submission_title,
            "firstname": get_name(speaker, "there"),
            "invitationlink": invitation_url,
        },
    )


def handle_new_schedule_invitation_answer(data):
    from schedule.models import ScheduleItem

    schedule_item = ScheduleItem.objects.get(id=data["schedule_item_id"])
    conference = schedule_item.conference
    speaker = schedule_item.submission.speaker

    user_name = get_name(speaker)

    invitation_admin_url = data["invitation_admin_url"]
    schedule_item_admin_url = data["schedule_item_admin_url"]

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


def handle_speaker_voucher_email_sent(data):
    from conferences.models import SpeakerVoucher

    speaker_voucher = SpeakerVoucher.objects.get(id=data["speaker_voucher_id"])

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


def handle_speaker_communication_sent(data):
    from conferences.models import Conference

    user_id = data["user_id"]
    user = User.objects.get(id=user_id)

    subject = data["subject"]
    body = data["body"]
    only_speakers_without_ticket = data["only_speakers_without_ticket"]

    conference_id = data["conference_id"]
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


def handle_volunteers_push_notification_sent(data):
    from volunteers_notifications.models import Notification, VolunteerDevice

    notification_id = data["notification_id"]
    volunteers_device_id = data["volunteers_device_id"]

    notification = Notification.objects.get(id=notification_id)
    device = VolunteerDevice.objects.get(id=volunteers_device_id)

    sns = boto3.client("sns")
    try:
        logger.info(
            "Publishing notification_id=%s to device_id=%s", notification_id, device.id
        )
        sns.publish(
            TargetArn=device.endpoint_arn,
            Message=json.dumps(
                {
                    "default": notification.body,
                    "APNS": json.dumps(
                        {
                            "aps": {
                                "alert": {
                                    "title": notification.title,
                                    "body": notification.body,
                                },
                                "sound": "default",
                            },
                        }
                    ),
                    "GCM": json.dumps(
                        {
                            "title": notification.title,
                            "message": notification.body,
                        },
                    ),
                }
            ),
            MessageStructure="json",
        )
    except (
        sns.exceptions.EndpointDisabledException,
        sns.exceptions.InvalidParameterException,
    ) as e:
        logger.warning(
            "Known error sending push notification_id=%s to device_id=%s",
            notification_id,
            device.id,
            exc_info=e,
        )
    except Exception as e:
        logger.warning(
            "Failed to push notification_id=%s to device_id=%s",
            notification_id,
            device.id,
            exc_info=e,
        )
        raise


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


def handle_proposal_rejected_sent(data):
    from submissions.models import Submission

    submission = Submission.objects.get(id=data["proposal_id"])
    submission_speaker = submission.speaker

    language_code = submission.languages.first().code
    conference_name = submission.conference.name.localize(language_code)

    send_email(
        template=EmailTemplate.SUBMISSION_REJECTED,
        to=submission_speaker.email,
        subject=f"[{conference_name}] Update about your proposal",
        variables={
            "firstname": get_name(submission_speaker, "there"),
            "conferenceName": conference_name,
            "submissionTitle": submission.title.localize(language_code),
            "submissionType": submission.type.name,
        },
    )


HANDLERS = {
    "NewCFPSubmission": handle_new_cfp_submission,
    "ScheduleInvitationSent": handle_schedule_invitation_sent,
    "ScheduleInvitationReminderSent": handle_schedule_invitation_sent,
    "NewScheduleInvitationAnswer": handle_new_schedule_invitation_answer,
    "SubmissionTimeSlotChanged": handle_submission_time_slot_changed,
    "SpeakerVoucherEmailSent": handle_speaker_voucher_email_sent,
    "SpeakerCommunicationSent": handle_speaker_communication_sent,
    "VolunteersPushNotificationSent": handle_volunteers_push_notification_sent,
    "ProposalRejectedSent": handle_proposal_rejected_sent,
}
