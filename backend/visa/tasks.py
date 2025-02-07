from django.urls import reverse
from notifications.models import EmailTemplate, EmailTemplateIdentifier
from pycon.signing import sign_path
from integrations import slack
import time
from django.template import Template, Context

import io
import tempfile

from association_membership.handlers.pretix.api import PretixAPI
from pycon.celery_utils import OnlyOneAtTimeTask
from visa.models import (
    InvitationLetterRequest,
    InvitationLetterRequestStatus,
)
from pycon.celery import app
from pypdf import PdfWriter
from django.core.files.base import ContentFile
from django.utils import timezone
from weasyprint import HTML
from django.template.loader import render_to_string

import logging

logger = logging.getLogger(__name__)


def process_invitation_letter_request_failed(self, exc, task_id, args, kwargs, einfo):
    invitation_letter_request_id = kwargs["invitation_letter_request_id"]

    invitation_letter_request = InvitationLetterRequest.objects.get(
        id=invitation_letter_request_id
    )
    invitation_letter_request.status = InvitationLetterRequestStatus.FAILED_TO_GENERATE
    invitation_letter_request.save(update_fields=["status"])

    logger.exception(
        "Failed to generate invitation letter for invitation_letter_request_id=%s",
        invitation_letter_request_id,
        exc_info=exc,
    )


@app.task(
    base=OnlyOneAtTimeTask,
    on_failure=process_invitation_letter_request_failed,
)
def process_invitation_letter_request(*, invitation_letter_request_id: int):
    invitation_letter_request = InvitationLetterRequest.objects.filter(
        id=invitation_letter_request_id,
        status__in=[
            InvitationLetterRequestStatus.PENDING,
            InvitationLetterRequestStatus.FAILED_TO_GENERATE,
        ],
    ).first()

    if not invitation_letter_request:
        return

    invitation_letter_request.status = InvitationLetterRequestStatus.PROCESSING
    invitation_letter_request.save(update_fields=["status"])

    config = invitation_letter_request.get_config()

    merger = PdfWriter()

    for attached_document in config.attached_documents.order_by("order").all():
        if not invitation_letter_request.can_include_document(attached_document):
            continue

        if attached_document.document:
            temp_file = attached_document.document.open()
        elif attached_document.dynamic_document:
            temp_file = render_dynamic_document(
                attached_document.dynamic_document, invitation_letter_request, config
            )
        else:
            logger.warning(
                "Invitation letter document id %s has no document or dynamic document",
                attached_document.id,
            )
            continue

        merger.append(temp_file)

    pretix_ticket = download_pretix_ticket(invitation_letter_request)
    merger.append(pretix_ticket)
    merger.compress_identical_objects(remove_identicals=True, remove_orphans=True)

    with tempfile.NamedTemporaryFile() as invitation_letter_file:
        merger.write(invitation_letter_file)
        merger.close()

        date_str = timezone.now().strftime("%Y-%m-%dT%H-%M-%S")

        invitation_letter_file.seek(0)
        invitation_letter_request.invitation_letter.save(
            f"invitation_letter_{date_str}.pdf",
            ContentFile(invitation_letter_file.read()),
        )
        invitation_letter_request.save()

    invitation_letter_request.status = InvitationLetterRequestStatus.PROCESSED
    invitation_letter_request.save(update_fields=["status", "invitation_letter"])


def render_dynamic_document(dynamic_document, invitation_letter_request, config):
    # strip is needed to convert from SafeString to str
    html_string = render_to_string(
        "visa/invitation-letter-dynamic-document.html",
        {
            "header": _render_content(
                dynamic_document["header"]["content"], invitation_letter_request, config
            ),
            "header_properties": dynamic_document["header"],
            "footer": _render_content(
                dynamic_document["footer"]["content"], invitation_letter_request, config
            ),
            "footer_properties": dynamic_document["footer"],
            "pages": [
                _render_content(page["content"], invitation_letter_request, config)
                for page in dynamic_document["pages"]
            ],
            "page_layout": dynamic_document["page_layout"],
        },
    ).strip()
    return io.BytesIO(HTML(string=html_string).write_pdf())


def _render_content(content, invitation_letter_request, config):
    inline_template = f"""
{{% load invitation_letter_asset %}}

{content}
"""
    template = Template(inline_template)
    return template.render(
        Context(
            {
                "config": config,
                # request info
                "full_name": invitation_letter_request.full_name,
                "nationality": invitation_letter_request.nationality,
                "address": invitation_letter_request.address,
                "date_of_birth": invitation_letter_request.date_of_birth,
                "passport_number": invitation_letter_request.passport_number,
                "embassy_name": invitation_letter_request.embassy_name,
                "role": invitation_letter_request.role,
                "grant_approved_type": invitation_letter_request.grant_approved_type,
                "has_accommodation_via_grant": invitation_letter_request.has_accommodation_via_grant(),
                "has_travel_via_grant": invitation_letter_request.has_travel_via_grant(),
                # conference
                "conference": invitation_letter_request.conference,
            }
        )
    )


def download_pretix_ticket(invitation_letter_request):
    pretix_api = PretixAPI.for_conference(invitation_letter_request.conference)
    attendee_tickets = pretix_api.get_all_attendee_tickets(
        invitation_letter_request.email
    )
    attendee_ticket = next(
        (ticket for ticket in attendee_tickets if ticket["item"]["admission"]), None
    )
    assert attendee_ticket, "No attendee ticket found"

    ticket_url = attendee_ticket["downloads"][0]["url"]

    attempts = 0

    while True:
        attempts += 1

        response = pretix_api.run_request(ticket_url)
        if response.status_code == 409 and attempts <= 3:
            time.sleep(2 * attempts)
            continue

        response.raise_for_status()
        break

    return io.BytesIO(response.content)


@app.task
def notify_new_invitation_letter_request_on_slack(
    *, invitation_letter_request_id: int, admin_absolute_uri: str
):
    invitation_letter_request = InvitationLetterRequest.objects.get(
        id=invitation_letter_request_id
    )
    conference = invitation_letter_request.conference
    name = invitation_letter_request.full_name

    admin_path = reverse(
        "admin:visa_invitationletterrequest_change", args=[invitation_letter_request.id]
    )

    slack.send_message(
        [
            {
                "type": "section",
                "text": {
                    "text": f"New invitation letter request from {name}",
                    "type": "plain_text",
                },
            }
        ],
        [
            {
                "blocks": [
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Open in Admin",
                                    "emoji": True,
                                },
                                "action_id": "ignore-action",
                                "url": f"{admin_absolute_uri}{admin_path[1:]}",
                            }
                        ],
                    }
                ]
            }
        ],
        oauth_token=conference.get_slack_oauth_token(),
        channel_id=conference.slack_new_invitation_letter_request_channel_id,
    )


@app.task
def send_invitation_letter_via_email(*, invitation_letter_request_id: int):
    invitation_letter_request = InvitationLetterRequest.objects.get(
        id=invitation_letter_request_id
    )

    conference = invitation_letter_request.conference

    download_invitation_letter_path = reverse(
        "download-invitation-letter", args=[invitation_letter_request.id]
    )
    signed_path = sign_path(download_invitation_letter_path)

    invitation_letter_download_url = f"https://admin.pycon.it{signed_path}"

    email_template = EmailTemplate.objects.for_conference(conference).get_by_identifier(
        EmailTemplateIdentifier.visa_invitation_letter_download
    )
    email_template.send_email(
        recipient_email=invitation_letter_request.email,
        placeholders={
            "invitation_letter_download_url": invitation_letter_download_url,
        },
    )

    invitation_letter_request.status = InvitationLetterRequestStatus.SENT
    invitation_letter_request.save(update_fields=["status"])
