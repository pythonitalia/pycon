import time
from django.template import Template, Context

import io
import tempfile

import requests
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
    autoretry_for=(requests.exceptions.HTTPError,),
    retry_backoff=True,
    max_retries=3,
    default_retry_delay=1,
)
def process_invitation_letter_request(*, invitation_letter_request_id: int):
    invitation_letter_request = (
        InvitationLetterRequest.objects.not_processed()
        .not_processing()
        .filter(id=invitation_letter_request_id)
        .first()
    )

    if not invitation_letter_request:
        return

    invitation_letter_request.status = InvitationLetterRequestStatus.PROCESSING
    invitation_letter_request.save(update_fields=["status"])

    config = invitation_letter_request.get_config()

    merger = PdfWriter()

    for attached_document in config.attached_documents.order_by("order").all():
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
                dynamic_document["header"], invitation_letter_request, config
            ),
            "footer": _render_content(
                dynamic_document["footer"], invitation_letter_request, config
            ),
            "pages": [
                _render_content(page["content"], invitation_letter_request, config)
                for page in dynamic_document["pages"]
            ],
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
