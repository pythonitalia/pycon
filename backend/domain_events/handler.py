import json
import logging
from datetime import timedelta
from urllib.parse import urljoin

import boto3
from asgiref.sync import async_to_sync
from django.conf import settings
from django.utils import timezone
from pythonit_toolkit.emails.templates import EmailTemplate
from pythonit_toolkit.emails.utils import mark_safe
from pythonit_toolkit.service_client import ServiceClient

from grants.models import Grant
from integrations import plain, slack
from notifications.emails import send_email

logger = logging.getLogger(__name__)

USERS_NAMES_FROM_IDS = """query UserNamesFromIds($ids: [ID!]!) {
    usersByIds(ids: $ids) {
        id
        fullname
        name
        username
        email
    }
}"""


def execute_service_client_query(query, variables):
    client = ServiceClient(
        url=f"{settings.USERS_SERVICE_URL}/internal-api",
        service_name="users-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    return async_to_sync(client.execute)(query, variables)


def get_name(user_data, fallback: str = "<no name specified>"):
    return (
        user_data["fullname"] or user_data["name"] or user_data["username"] or fallback
    )


def handle_grant_reply_approved_sent(data):
    logger.info("Sending Reply APPROVED email for Grant %s", data["grant_id"])
    is_reminder = data["is_reminder"]
    grant = Grant.objects.get(id=data["grant_id"])
    reply_url = urljoin(settings.FRONTEND_URL, "/grants/reply/")

    subject = (
        "Reminder: Financial Aid Update" if is_reminder else "Financial Aid Update"
    )

    template = None
    variables = {
        "replyLink": reply_url,
        "startDate": f"{grant.conference.start:%-d %B}",
        "endDate": f"{grant.conference.end+timedelta(days=1):%-d %B}",
        "deadlineDateTime": f"{grant.applicant_reply_deadline:%-d %B %Y %H:%M %Z}",
        "deadlineDate": f"{grant.applicant_reply_deadline:%-d %B %Y}",
    }
    if grant.approved_type == Grant.ApprovedType.ticket_only:
        template = EmailTemplate.GRANT_APPROVED_TICKET_ONLY

    elif grant.approved_type == Grant.ApprovedType.ticket_accommodation:
        template = EmailTemplate.GRANT_APPROVED_TICKET_ACCOMMODATION
    elif grant.approved_type == Grant.ApprovedType.ticket_travel:
        template = EmailTemplate.GRANT_APPROVED_TICKET_TRAVEL

    elif grant.approved_type == Grant.ApprovedType.ticket_travel_accommodation:
        if grant.travel_amount == 0:
            raise ValueError(
                "Grant travel amount is set to Zero, can't send the email!"
            )

        template = EmailTemplate.GRANT_APPROVED_TICKET_TRAVEL_ACCOMMODATION
        variables["amount"] = f"{grant.travel_amount:.0f}"
    else:
        raise ValueError(f"Grant Approved type `{grant.approved_type}` not valid.")

    _send_grant_email(template=template, subject=subject, grant=grant, **variables)

    grant.status = Grant.Status.waiting_for_confirmation
    grant.save()

    logger.info("Email sent for Grant %s", grant.id)


def handle_grant_reply_waiting_list_sent(data):
    logger.info("Sending Reply WAITING LIST email for Grant %s", data["grant_id"])

    _send_grant_waiting_list_email(data, template=EmailTemplate.GRANT_WAITING_LIST)


def handle_grant_reply_waiting_list_update_sent(data):
    logger.info(
        "Sending Reply WAITING LIST UPDATE email for Grant %s", data["grant_id"]
    )

    _send_grant_waiting_list_email(
        data, template=EmailTemplate.GRANT_WAITING_LIST_UPDATE
    )


def _send_grant_waiting_list_email(data, template):
    grant = Grant.objects.get(id=data["grant_id"])
    reply_url = urljoin(settings.FRONTEND_URL, "/grants/reply/")

    subject = "Financial Aid Update"
    deadline = grant.conference.deadlines.filter(
        type="custom", name__contains={"en": "Update Grants in Waiting List"}
    ).first()

    _send_grant_email(
        template=template,
        subject=subject,
        grant=grant,
        replyLink=reply_url,
        grantsUpdateDeadline=f"{deadline.start:%-d %B %Y}",
    )

    logger.info("Email sent for Grant %s", grant.id)


def handle_grant_reply_rejected_sent(data):
    logger.info("Sending Reply REJECTED email for Grant %s", data["grant_id"])
    grant = Grant.objects.get(id=data["grant_id"])

    subject = "Financial Aid Update"

    _send_grant_email(
        template=EmailTemplate.GRANT_REJECTED,
        subject=subject,
        grant=grant,
    )

    logger.info("Email sent for Grant %s", grant.id)


def _send_grant_email(template: EmailTemplate, subject: str, grant: Grant, **kwargs):
    try:
        users_result = execute_service_client_query(
            USERS_NAMES_FROM_IDS, {"ids": [grant.user_id]}
        )

        user_data = users_result.data["usersByIds"][0]
        conference_name = grant.conference.name.localize("en")
        subject_prefix = f"[{conference_name}]"

        send_email(
            template=template,
            to=user_data["email"],
            subject=f"{subject_prefix} {subject}",
            variables={
                "firstname": get_name(user_data, "there"),
                "conferenceName": conference_name,
                **kwargs,
            },
            reply_to=["grants@pycon.it"],
        )

        grant.applicant_reply_sent_at = timezone.now()
        grant.save()
    except Exception as e:
        logger.error(
            "Something went wrong while sending email Reply for Grant %s:\n%s",
            grant.id,
            e,
            exc_info=True,
        )


def handle_new_grant_reply(data):
    grant = Grant.objects.get(id=data["grant_id"])
    admin_url = data["admin_url"]

    actions = []
    if grant.applicant_message:
        actions.append("sent a message")
    if grant.status in (Grant.Status.confirmed, Grant.Status.refused):
        actions.append(f"{Grant.Status(grant.status).label} the grant")

    slack.send_message(
        [
            {
                "type": "section",
                "text": {
                    "text": f"{grant.full_name} {' and '.join(actions)}",
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
                            "text": f"*<{admin_url}|Open admin>*",
                        },
                    },
                ],
            },
        ],
        token=grant.conference.slack_new_grant_reply_incoming_incoming_webhook_url,
    )


def handle_new_plain_chat_sent(data):
    user_id = data["user_id"]
    message = data["message"]

    users_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [user_id]}
    )

    user_data = users_result.data["usersByIds"][0]
    name = get_name(user_data, "Financial Aid Appicant")
    plain.send_message(user_data, title=f"{name} has some questions:", message=message)


def handle_new_cfp_submission(data):
    from conferences.models import Conference

    title = data["title"]
    elevator_pitch = data["elevator_pitch"]
    submission_type = data["submission_type"]
    admin_url = data["admin_url"]
    tags = data["tags"]
    speaker_id = data["speaker_id"]

    conference = Conference.objects.get(id=data["conference_id"])

    user_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [speaker_id]}
    )
    user_data = user_result.data["usersByIds"][0]
    user_name = get_name(user_data)

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

    users_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [speaker_id]}
    )
    speaker_data = users_result.data["usersByIds"][0]
    prefix = "[PyCon Italia 2023]"
    subject = (
        f"{prefix} Reminder: Your submission was accepted, confirm your presence"
        if is_reminder
        else f"{prefix} Your submission was accepted!"
    )

    send_email(
        template=EmailTemplate.SUBMISSION_ACCEPTED,
        to=speaker_data["email"],
        subject=subject,
        variables={
            "submissionTitle": submission_title,
            "firstname": get_name(speaker_data, "there"),
            "invitationlink": invitation_url,
        },
    )


def handle_submission_time_slot_changed(data):
    speaker_id = data["speaker_id"]
    invitation_url = data["invitation_url"]
    submission_title = data["submission_title"]

    users_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [speaker_id]}
    )
    speaker_data = users_result.data["usersByIds"][0]

    send_email(
        template=EmailTemplate.SUBMISSION_SCHEDULE_TIME_CHANGED,
        to=speaker_data["email"],
        subject="[PyCon Italia 2023] Your Submission time slot has been changed!",
        variables={
            "submissionTitle": submission_title,
            "firstname": get_name(speaker_data, "there"),
            "invitationlink": invitation_url,
        },
    )


def handle_new_schedule_invitation_answer(data):
    from schedule.models import ScheduleItem

    schedule_item = ScheduleItem.objects.get(id=data["schedule_item_id"])
    conference = schedule_item.conference
    speaker_id = schedule_item.submission.speaker_id

    user_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [speaker_id]}
    )
    user_data = user_result.data["usersByIds"][0]
    user_name = get_name(user_data)

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

    speaker_id = speaker_voucher.user_id
    voucher_code = speaker_voucher.voucher_code

    users_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [speaker_id]}
    )
    speaker_data = users_result.data["usersByIds"][0]

    send_email(
        template=EmailTemplate.SPEAKER_VOUCHER_CODE,
        to=speaker_data["email"],
        subject="[PyCon Italia 2023] Your Speaker Voucher Code",
        variables={
            "firstname": get_name(speaker_data, "there"),
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
    user_id = data["user_id"]
    subject = data["subject"]
    body = data["body"]

    users_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [user_id]}
    )
    speaker_data = users_result.data["usersByIds"][0]

    send_email(
        template=EmailTemplate.SPEAKER_COMMUNICATION,
        to=speaker_data["email"],
        subject=f"[PyCon Italia 2023] {subject}",
        variables={
            "firstname": get_name(speaker_data, "there"),
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


HANDLERS = {
    "GrantReplyApprovedSent": handle_grant_reply_approved_sent,
    "GrantReplyApprovedReminderSent": handle_grant_reply_approved_sent,
    "GrantReplyWaitingListSent": handle_grant_reply_waiting_list_sent,
    "GrantReplyWaitingListUpdateSent": handle_grant_reply_waiting_list_update_sent,
    "GrantReplyRejectedSent": handle_grant_reply_rejected_sent,
    "NewGrantReply": handle_new_grant_reply,
    "NewPlainChatSent": handle_new_plain_chat_sent,
    "NewCFPSubmission": handle_new_cfp_submission,
    "ScheduleInvitationSent": handle_schedule_invitation_sent,
    "ScheduleInvitationReminderSent": handle_schedule_invitation_sent,
    "NewScheduleInvitationAnswer": handle_new_schedule_invitation_answer,
    "SubmissionTimeSlotChanged": handle_submission_time_slot_changed,
    "SpeakerVoucherEmailSent": handle_speaker_voucher_email_sent,
    "SpeakerCommunicationSent": handle_speaker_communication_sent,
    "VolunteersPushNotificationSent": handle_volunteers_push_notification_sent,
}
