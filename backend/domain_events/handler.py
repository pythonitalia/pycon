import json
import logging

import boto3
from asgiref.sync import async_to_sync
from django.conf import settings
from pythonit_toolkit.emails.templates import EmailTemplate
from pythonit_toolkit.emails.utils import mark_safe
from pythonit_toolkit.service_client import ServiceClient

from domain_events.publisher import publish_message
from integrations import slack
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
        url=f"{settings.USERS_SERVICE}/internal-api",
        service_name="users-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    return async_to_sync(client.execute)(query, variables)


def get_name(user_data, fallback: str = "<no name specified>"):
    return (
        user_data["fullname"] or user_data["name"] or user_data["username"] or fallback
    )


def handle_new_submission_comment(data):
    publish_message(
        "NewSubmissionComment/SlackNotification",
        body=data,
        deduplication_id=str(data["comment_id"]),
    )

    publish_message(
        "NewSubmissionComment/EmailNotification",
        body=data,
        deduplication_id=str(data["comment_id"]),
    )


def handle_send_email_notification_for_new_submission_comment(data):
    submission_title = data["submission_title"]
    author_id = data["author_id"]
    all_commenters_ids = data["all_commenters_ids"]
    submission_url = data["submission_url"]

    users_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": all_commenters_ids}
    )
    users_by_id = {int(user["id"]): user for user in users_result.data["usersByIds"]}

    # Notify everyone who commented on the submission
    # but not the person posting the comment
    commenters_to_notify = [
        commenter for commenter in all_commenters_ids if commenter != author_id
    ]

    for commenter_id in commenters_to_notify:
        commenter_data = users_by_id[commenter_id]
        send_email(
            template=EmailTemplate.NEW_COMMENT_ON_SUBMISSION,
            to=commenter_data["email"],
            subject=f"[PyCon Italia 2022] New comment on Submission {submission_title}",
            variables={
                "submissionTitle": submission_title,
                "userName": get_name(commenter_data, "there"),
                "submissionlink": submission_url,
            },
        )


def handle_send_slack_notification_for_new_submission_comment(data):
    speaker_id = data["speaker_id"]
    submission_title = data["submission_title"]
    author_id = data["author_id"]
    admin_url = data["admin_url"]
    submission_url = data["submission_url"]
    comment = data["comment"]

    users_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [speaker_id, author_id]}
    )
    users_by_id = {int(user["id"]): user for user in users_result.data["usersByIds"]}

    speaker_name = get_name(users_by_id[speaker_id])
    comment_author_name = get_name(users_by_id[author_id])

    slack.send_message(
        [
            {
                "type": "section",
                "text": {
                    "text": f"New comment on submission {submission_title}",
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
                            "text": f"*<{admin_url}|Open admin>* | *<{submission_url}|Open site>*",
                        },
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": "*Comment*"},
                    },
                    {
                        "type": "section",
                        "text": {"type": "plain_text", "text": comment, "emoji": False},
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": "*Submission Author*"},
                            {"type": "mrkdwn", "text": "*Comment Author*"},
                            {"type": "plain_text", "text": speaker_name},
                            {"type": "plain_text", "text": comment_author_name},
                            {"type": "mrkdwn", "text": "*Is Submission Author*"},
                            {
                                "type": "plain_text",
                                "text": "Yes" if speaker_id == author_id else "No",
                            },
                        ],
                    },
                ],
            },
        ],
        channel="submission-comments",
    )


def handle_new_cfp_submission(data):
    title = data["title"]
    elevator_pitch = data["elevator_pitch"]
    submission_type = data["submission_type"]
    admin_url = data["admin_url"]
    topic = data["topic"]
    duration = data["duration"]
    speaker_id = data["speaker_id"]

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
                    "text": f"New _{submission_type}_ Submission by {user_name}",
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
                            {"type": "mrkdwn", "text": "*Topic*"},
                            {"type": "mrkdwn", "text": "*Duration*"},
                            {"type": "mrkdwn", "text": str(topic)},
                            {"type": "plain_text", "text": str(duration)},
                        ],
                    }
                ]
            }
        ],
        channel="cfp",
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
    subject = (
        "[PyCon Italia 2022] Reminder: Your submission was accepted, confirm your presence"
        if is_reminder
        else "[PyCon Italia 2022] Your submission was accepted!"
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
        subject="[PyCon Italia 2022] Your Submission time slot has been changed!",
        variables={
            "submissionTitle": submission_title,
            "firstname": get_name(speaker_data, "there"),
            "invitationlink": invitation_url,
        },
    )


def handle_new_schedule_invitation_answer(data):
    speaker_id = data["speaker_id"]
    submission_title = data["submission_title"]
    answer = data["answer"]
    speaker_notes = data["speaker_notes"]
    time_slot = data["time_slot"]
    invitation_admin_url = data["invitation_admin_url"]
    schedule_item_admin_url = data["schedule_item_admin_url"]

    users_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [speaker_id]}
    )
    speaker_data = users_result.data["usersByIds"][0]

    send_email(
        template=EmailTemplate.NEW_SCHEDULE_INVITATION_ANSWER,
        to=settings.SPEAKERS_EMAIL_ADDRESS,
        subject=f"[PyCon Italia 2022] Schedule Invitation Answer: {submission_title}",
        variables={
            "submissionTitle": submission_title,
            "speakerName": get_name(speaker_data),
            "speakerEmail": speaker_data["email"],
            "timeSlot": time_slot,
            "answer": answer,
            "notes": speaker_notes,
            "invitationAdminUrl": invitation_admin_url,
            "scheduleItemAdminUrl": schedule_item_admin_url,
        },
        reply_to=[
            speaker_data["email"],
        ],
    )


def handle_speaker_voucher_email_sent(data):
    speaker_id = data["speaker_id"]
    voucher_code = data["voucher_code"]

    users_result = execute_service_client_query(
        USERS_NAMES_FROM_IDS, {"ids": [speaker_id]}
    )
    speaker_data = users_result.data["usersByIds"][0]

    send_email(
        template=EmailTemplate.SPEAKER_VOUCHER_CODE,
        to=speaker_data["email"],
        subject="[PyCon Italia 2022] Your Speaker Voucher Code",
        variables={
            "firstname": get_name(speaker_data, "there"),
            "voucherCode": voucher_code,
        },
        reply_to=[
            settings.SPEAKERS_EMAIL_ADDRESS,
        ],
    )


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
        subject=f"[PyCon Italia 2022] {subject}",
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


HANDLERS = {
    "NewSubmissionComment/SlackNotification": handle_send_slack_notification_for_new_submission_comment,
    "NewSubmissionComment/EmailNotification": handle_send_email_notification_for_new_submission_comment,
    "NewSubmissionComment": handle_new_submission_comment,
    "NewCFPSubmission": handle_new_cfp_submission,
    "ScheduleInvitationSent": handle_schedule_invitation_sent,
    "ScheduleInvitationReminderSent": handle_schedule_invitation_sent,
    "NewScheduleInvitationAnswer": handle_new_schedule_invitation_answer,
    "SubmissionTimeSlotChanged": handle_submission_time_slot_changed,
    "SpeakerVoucherEmailSent": handle_speaker_voucher_email_sent,
    "SpeakerCommunicationSent": handle_speaker_communication_sent,
    "VolunteersPushNotificationSent": handle_volunteers_push_notification_sent,
}
