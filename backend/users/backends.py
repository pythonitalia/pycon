from visa.models import InvitationLetterDocument
from conferences.models.conference import Conference
from django.contrib.auth.backends import ModelBackend
from django.db.models.base import Model
from users.models import User


class PermissionsBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        return None

    def has_perm(self, user_obj: User, perm: str, obj: Model | None = None) -> bool:
        if not obj:
            return False

        has_conference_permission = user_obj.is_superuser
        conference_id = self._get_conference_id(obj)

        if user_obj.admin_all_conferences:
            has_conference_permission = True
        elif user_obj.admin_conferences.filter(id=conference_id).exists():
            has_conference_permission = True

        parent_permissions = super().has_perm(user_obj, perm)
        return has_conference_permission and parent_permissions

    def _get_conference_id(self, obj: Model) -> int:
        match obj:
            case Conference():
                return obj.id
            case InvitationLetterDocument():
                return obj.invitation_letter_conference_config.conference_id
            case _:
                return obj.conference_id
