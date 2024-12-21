from api.context import Context
from custom_admin.audit import create_change_admin_log_entry
from visa.models import InvitationLetterDocument as InvitationLetterDocumentModel
from api.visa.permissions import CanEditInvitationLetterDocument
from strawberry.tools import create_type
from api.visa.types import InvitationLetterDocument
import strawberry


@strawberry.input
class UpdateInvitationLetterDocumentPageInput:
    id: strawberry.ID
    title: str
    content: str


@strawberry.input
class UpdateInvitationLetterDocumentStructureInput:
    header: str
    footer: str
    pages: list[UpdateInvitationLetterDocumentPageInput]


@strawberry.input
class UpdateInvitationLetterDocumentInput:
    id: strawberry.ID
    dynamic_document: UpdateInvitationLetterDocumentStructureInput


@strawberry.field(permission_classes=[CanEditInvitationLetterDocument])
def update_invitation_letter_document(
    info: strawberry.Info[Context], input: UpdateInvitationLetterDocumentInput
) -> InvitationLetterDocument:
    invitation_letter_document = InvitationLetterDocumentModel.objects.filter(
        id=input.id
    ).first()

    if not invitation_letter_document:
        raise ValueError("Invitation letter document not found")

    if invitation_letter_document.document:
        raise ValueError("Invitation letter document has a file attached")

    invitation_letter_document.dynamic_document = strawberry.asdict(
        input.dynamic_document
    )
    invitation_letter_document.save(update_fields=["dynamic_document"])

    create_change_admin_log_entry(
        info.context.request.user,
        invitation_letter_document,
        change_message="Invitation letter document updated",
    )
    return InvitationLetterDocument.from_model(invitation_letter_document)


VisaMutation = create_type(
    "VisaMutation",
    (update_invitation_letter_document,),
)
