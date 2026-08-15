from api.permissions import IsStaffPermission
from visa.models import InvitationLetterDocument


class CanViewInvitationLetterDocument(IsStaffPermission):
    message = "Cannot view invitation letter document"

    def has_permission(self, source, info, **kwargs):
        if not super().has_permission(source, info, **kwargs):
            return False

        self.invitation_letter_document = self.get_invitation_letter_document(kwargs)
        user = info.context.request.user
        return user.has_perm(
            "visa.view_invitationletterdocument", self.invitation_letter_document
        )

    def get_invitation_letter_document(self, kwargs):
        if input := kwargs.get("input", None):
            id = input.id
        else:
            id = kwargs.get("id")

        return InvitationLetterDocument.objects.filter(id=id).first()


class CanEditInvitationLetterDocument(CanViewInvitationLetterDocument):
    message = "Cannot edit invitation letter document"

    def has_permission(self, source, info, **kwargs):
        if not super().has_permission(source, info, **kwargs):
            return False

        invitation_letter_document = self.invitation_letter_document
        user = info.context.request.user
        return user.has_perm(
            "visa.change_invitationletterdocument", invitation_letter_document
        )
