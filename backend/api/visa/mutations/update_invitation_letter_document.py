from typing import Annotated
from api.context import Context
from api.types import NotFound
from custom_admin.audit import create_change_admin_log_entry
from visa.models import InvitationLetterDocument as InvitationLetterDocumentModel
from api.visa.permissions import CanEditInvitationLetterDocument
from api.visa.types import InvitationLetterDocument
import strawberry


@strawberry.input
class UpdateInvitationLetterDocumentPageInput:
    id: strawberry.ID
    title: str
    content: str


@strawberry.input
class UpdateInvitationLetterDocumentRunningPartInput:
    content: str
    align: str
    margin: str


@strawberry.input
class UpdateInvitationLetterDocumentPageLayoutInput:
    margin: str


@strawberry.input
class UpdateInvitationLetterDocumentStructureInput:
    header: UpdateInvitationLetterDocumentRunningPartInput
    footer: UpdateInvitationLetterDocumentRunningPartInput
    page_layout: UpdateInvitationLetterDocumentPageLayoutInput
    pages: list[UpdateInvitationLetterDocumentPageInput]


@strawberry.input
class UpdateInvitationLetterDocumentInput:
    id: strawberry.ID
    dynamic_document: UpdateInvitationLetterDocumentStructureInput


@strawberry.type
class InvitationLetterDocumentNotEditable:
    message: str = "Invitation letter document is not editable"


UpdateInvitationLetterDocumentResult = Annotated[
    InvitationLetterDocument | InvitationLetterDocumentNotEditable | NotFound,
    strawberry.union(name="UpdateInvitationLetterDocumentResult"),
]


@strawberry.field(permission_classes=[CanEditInvitationLetterDocument])
def update_invitation_letter_document(
    info: strawberry.Info[Context], input: UpdateInvitationLetterDocumentInput
) -> UpdateInvitationLetterDocumentResult:
    invitation_letter_document = InvitationLetterDocumentModel.objects.filter(
        id=input.id,
    ).first()

    if not invitation_letter_document:
        return NotFound()

    if invitation_letter_document.document:
        return InvitationLetterDocumentNotEditable()

    new_document_data = strawberry.asdict(input.dynamic_document)
    if invitation_letter_document.dynamic_document != new_document_data:
        invitation_letter_document.dynamic_document = new_document_data
        invitation_letter_document.save(update_fields=["dynamic_document"])

        config = invitation_letter_document.invitation_letter_conference_config

        create_change_admin_log_entry(
            info.context.request.user,
            config,
            change_message=f"Updated the content of dynamic document {invitation_letter_document.name}",
        )

    return InvitationLetterDocument.from_model(invitation_letter_document)
