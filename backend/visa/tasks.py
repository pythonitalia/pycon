import tempfile
from visa.models import (
    InvitationLetterOrganizerConfig,
    InvitationLetterRequest,
    InvitationLetterRequestStatus,
)
from pycon.celery import app
from pypdf import PdfWriter
from django.core.files.base import ContentFile
from django.utils import timezone


# @app.task(base=OnlyOneAtTimeTask)
@app.task()
def process_invitation_letter_request(*, invitation_letter_request_id: int):
    invitation_letter_request = InvitationLetterRequest.objects.filter(
        id=invitation_letter_request_id, status=InvitationLetterRequestStatus.PENDING
    ).first()

    if not invitation_letter_request:
        return

    # invitation_letter_request.status = InvitationLetterRequestStatus.PROCESSING
    # invitation_letter_request.save(update_fields=['status'])

    config = InvitationLetterOrganizerConfig.objects.get(
        organizer=invitation_letter_request.conference.organizer
    )

    merger = PdfWriter()

    for attached_document in config.attached_documents.order_by("order").all():
        temp_file = attached_document.document.open()
        merger.append(temp_file)

    with tempfile.NamedTemporaryFile() as invitation_letter_file:
        merger.write(invitation_letter_file)
        merger.close()

        date_str = timezone.now().strftime("%Y-%m-%dT%H-%M-%S")

        invitation_letter_file.seek(0)
        invitation_letter_request.invitation_letter.save(
            f"invitation_letter_{date_str}.pdf",
            ContentFile(invitation_letter_file.read()),
        )
