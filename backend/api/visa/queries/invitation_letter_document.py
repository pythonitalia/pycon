from api.visa.permissions import CanViewInvitationLetterDocument
from visa.models import InvitationLetterDocument as InvitationLetterDocumentModel
from api.visa.types import InvitationLetterDocument
import strawberry


@strawberry.field(permission_classes=[CanViewInvitationLetterDocument])
def invitation_letter_document(id: strawberry.ID) -> InvitationLetterDocument | None:
    if invitation_letter_document := InvitationLetterDocumentModel.objects.filter(
        id=id
    ).first():
        return InvitationLetterDocument.from_model(invitation_letter_document)

    return None
