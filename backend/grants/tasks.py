import logging
from datetime import timedelta
from urllib.parse import urljoin

from django.conf import settings
from django.utils import timezone

from grants.models import Grant
from integrations import slack
from notifications.models import EmailTemplate, EmailTemplateIdentifier
from pycon.celery import app
from users.models import User

logger = logging.getLogger(__name__)


def get_name(user: User | None, fallback: str = "<no name specified>") -> str:
    if not user:
        return fallback

    return user.full_name or user.name or user.username or fallback


@app.task
def send_grant_reply_approved_email(*, grant_id: int, is_reminder: bool) -> None:
    logger.info("Sending Reply APPROVED email for Grant %s", grant_id)
    grant = Grant.objects.get(id=grant_id)

    total_amount = grant.total_grantee_reimbursement_amount
    ticket_only = grant.has_ticket_only()

    if total_amount == 0 and not ticket_only:
        raise ValueError(
            f"Grant {grant_id} has no reimbursement amount and is not ticket-only. "
            "This indicates missing or zero-amount reimbursements."
        )

    reply_url = urljoin(settings.FRONTEND_URL, "/grants/reply/")

    variables = {
        "reply_url": reply_url,
        "start_date": f"{grant.conference.start:%-d %B}",
        "end_date": f"{grant.conference.end + timedelta(days=1):%-d %B}",
        "deadline_date_time": f"{grant.applicant_reply_deadline:%-d %B %Y %H:%M %Z}",
        "deadline_date": f"{grant.applicant_reply_deadline:%-d %B %Y}",
        "visa_page_link": urljoin(settings.FRONTEND_URL, "/visa"),
        "total_amount": f"{total_amount:.0f}" if total_amount > 0 else None,
        "ticket_only": ticket_only,
        "is_reminder": is_reminder,
    }

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

    _send_grant_waiting_list_email(
        grant_id, template_identifier=EmailTemplateIdentifier.grant_waiting_list
    )


@app.task
def send_grant_reply_waiting_list_update_email(*, grant_id):
    logger.info("Sending Reply WAITING LIST UPDATE email for Grant %s", grant_id)

    _send_grant_waiting_list_email(
        grant_id, template_identifier=EmailTemplateIdentifier.grant_waiting_list_update
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


def _send_grant_waiting_list_email(grant_id, template_identifier):
    grant = Grant.objects.get(id=grant_id)
    reply_url = urljoin(settings.FRONTEND_URL, "/grants/reply/")

    deadline = grant.conference.deadlines.filter(
        type="grants_waiting_list_update"
    ).first()

    if not deadline:
        logger.error(
            f"No grants_waiting_list_update deadline found for conference {grant.conference}"
        )
        raise ValueError(
            f"Conference {grant.conference.code} missing grants_waiting_list_update deadline"
        )

    _new_send_grant_email(
        template_identifier=template_identifier,
        grant=grant,
        placeholders={
            "reply_url": reply_url,
            "grants_update_deadline": f"{deadline.start:%-d %B %Y}",
        },
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
