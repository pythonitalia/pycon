from datetime import timedelta
from urllib.parse import urljoin

from django.conf import settings
from django.utils import timezone
from notifications.models import EmailTemplateIdentifier
from notifications.templates import EmailTemplate

from users.models import User
from grants.models import Grant
from integrations import slack
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

    variables = {
        "reply_url": reply_url,
        "start_date": f"{grant.conference.start:%-d %B}",
        "end_date": f"{grant.conference.end+timedelta(days=1):%-d %B}",
        "deadline_date_time": f"{grant.applicant_reply_deadline:%-d %B %Y %H:%M %Z}",
        "deadline_date": f"{grant.applicant_reply_deadline:%-d %B %Y}",
        "visa_page_link": urljoin(settings.FRONTEND_URL, "/visa"),
        "has_approved_travel": grant.has_approved_travel(),
        "has_approved_accommodation": grant.has_approved_accommodation(),
        "is_reminder": is_reminder,
    }

    if grant.has_approved_travel():
        if not grant.travel_amount:
            raise ValueError(
                "Grant travel amount is set to Zero, can't send the email!"
            )

        variables["travel_amount"] = f"{grant.travel_amount:.0f}"

    _new_send_grant_email(
        template_identifier=EmailTemplateIdentifier.grant_approved,
        grant=grant,
        placeholders=variables,
    )

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

    _new_send_grant_email(
        template_identifier=EmailTemplateIdentifier.grant_rejected,
        grant=grant,
        placeholders={},
    )

    logger.info("Rejection email sent for Grant %s", grant.id)


@app.task
def notify_new_grant_reply_slack(*, grant_id, admin_url):
    grant = Grant.objects.get(id=grant_id)

    actions = []
    if grant.status in (Grant.Status.confirmed, Grant.Status.refused):
        actions.append(f"{Grant.Status(grant.status).label} the grant")

    conference = grant.conference

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
        oauth_token=conference.get_slack_oauth_token(),
        channel_id=conference.slack_new_grant_reply_channel_id,
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
            "hasApprovedAccommodation": grant.has_approved_accommodation(),
            "visaPageLink": urljoin(settings.FRONTEND_URL, "/visa"),
        },
        reply_to=[
            "grants@pycon.it",
        ],
    )

    grant.voucher_email_sent_at = timezone.now()
    grant.save()


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


def _new_send_grant_email(
    template_identifier: EmailTemplateIdentifier, grant: Grant, placeholders
):
    conference = grant.conference
    user = grant.user
    conference_name = grant.conference.name.localize("en")

    email_template = EmailTemplate.objects.for_conference(conference).get_by_identifier(
        template_identifier
    )

    email_template.send_email(
        recipient=user,
        placeholders={
            "conference_name": conference_name,
            "user_name": get_name(user, "there"),
            **placeholders,
        },
    )

    grant.applicant_reply_sent_at = timezone.now()
    grant.save()


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
