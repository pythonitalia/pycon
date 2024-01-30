from datetime import timedelta
from urllib.parse import urljoin

from django.conf import settings
from django.utils import timezone
from pythonit_toolkit.emails.templates import EmailTemplate

from users.models import User
from grants.models import Grant
from integrations import plain, slack
from notifications.emails import send_email

import logging

from pycon.celery import app

logger = logging.getLogger(__name__)


def get_name(user: User, fallback: str = "<no name specified>"):
    return user.full_name or user.name or user.username or fallback


@app.task
def send_grant_reply_approved_email(*, grant_id, is_reminder):
    logger.info("Sending Reply APPROVED email for Grant %s", grant_id)
    grant = Grant.objects.get(id=grant_id)
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
    elif grant.approved_type == Grant.ApprovedType.ticket_travel:
        template = EmailTemplate.GRANT_APPROVED_TICKET_TRAVEL
        if grant.travel_amount == 0:
            raise ValueError(
                "Grant travel amount is set to Zero, can't send the email!"
            )

        variables["amount"] = f"{grant.travel_amount:.0f}"
    elif grant.approved_type == Grant.ApprovedType.ticket_accommodation:
        template = EmailTemplate.GRANT_APPROVED_TICKET_ACCOMMODATION
    elif grant.approved_type == Grant.ApprovedType.ticket_travel_accommodation:
        template = EmailTemplate.GRANT_APPROVED_TICKET_TRAVEL_ACCOMMODATION
        if grant.travel_amount == 0:
            raise ValueError(
                "Grant travel amount is set to Zero, can't send the email!"
            )

        variables["amount"] = f"{grant.travel_amount:.0f}"
    else:
        raise ValueError(f"Grant Approved type `{grant.approved_type}` not valid.")

    _send_grant_email(template=template, subject=subject, grant=grant, **variables)

    grant.status = Grant.Status.waiting_for_confirmation
    grant.save()

    logger.info("Email sent for Grant %s", grant.id)


@app.task
def send_grant_reply_waiting_list_email(*, grant_id):
    logger.info("Sending Reply WAITING LIST email for Grant %s", grant_id)

    _send_grant_waiting_list_email(grant_id, template=EmailTemplate.GRANT_WAITING_LIST)


@app.task
def send_grant_reply_waiting_list_update_email(*, grant_id):
    logger.info("Sending Reply WAITING LIST UPDATE email for Grant %s", grant_id)

    _send_grant_waiting_list_email(
        grant_id, template=EmailTemplate.GRANT_WAITING_LIST_UPDATE
    )


@app.task
def send_grant_reply_rejected_email(grant_id):
    logger.info("Sending Reply REJECTED email for Grant %s", grant_id)
    grant = Grant.objects.get(id=grant_id)

    subject = "Financial Aid Update"

    _send_grant_email(
        template=EmailTemplate.GRANT_REJECTED,
        subject=subject,
        grant=grant,
    )

    logger.info("Email sent for Grant %s", grant.id)


@app.task
def notify_new_grant_reply_slack(*, grant_id, admin_url):
    grant = Grant.objects.get(id=grant_id)

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


@app.task
def send_grant_voucher_email(*, grant_id):
    grant = Grant.objects.get(id=grant_id)

    user = grant.user
    voucher_code = grant.voucher_code

    conference_name = grant.conference.name.localize("en")
    subject_prefix = f"[{conference_name}]"

    send_email(
        template=EmailTemplate.GRANT_VOUCHER_CODE,
        to=user.email,
        subject=f"{subject_prefix} Your Grant Voucher Code",
        variables={
            "firstname": get_name(user, "there"),
            "voucherCode": voucher_code,
        },
        reply_to=[
            "grants@pycon.it",
        ],
    )

    grant.voucher_email_sent_at = timezone.now()
    grant.save()


@app.task
def send_new_plain_chat(*, user_id, message):
    if not settings.PLAIN_API:
        return

    user = User.objects.get(id=user_id)

    name = get_name(user, "Financial Aid Applicant")
    thread_id = plain.send_message(
        user, title=f"{name} has some questions:", message=message
    )

    try:
        grant = Grant.objects.get(user=user)
        grant.plain_thread_id = thread_id
        grant.save()
    except Grant.DoesNotExist:
        logger.error("Couldn't find the grant for: %s", user.user_id)


def _send_grant_waiting_list_email(grant_id, template):
    grant = Grant.objects.get(id=grant_id)
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


def _send_grant_email(template: EmailTemplate, subject: str, grant: Grant, **kwargs):
    try:
        user = grant.user

        conference_name = grant.conference.name.localize("en")
        subject_prefix = f"[{conference_name}]"

        send_email(
            template=template,
            to=user.email,
            subject=f"{subject_prefix} {subject}",
            variables={
                "firstname": get_name(user, "there"),
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
