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
        conference_id = obj.conference_id

        if user_obj.admin_all_conferences:
            has_conference_permission = True
        elif user_obj.admin_conferences.filter(id=conference_id).exists():
            has_conference_permission = True

        parent_permissions = super().has_perm(user_obj, perm)
        return has_conference_permission and parent_permissions
