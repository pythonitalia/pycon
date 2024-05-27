from typing import TYPE_CHECKING
from files_upload.upload import check_user_can_upload
from strawberry.permission import BasePermission

if TYPE_CHECKING:
    from api.files_upload.mutations.upload_file import UploadFileInput


class IsFileTypeUploadAllowed(BasePermission):
    message = "You cannot upload files of this type"

    def has_permission(self, source, info, input: "UploadFileInput", **kwargs):
        type = input.type
        user = info.context.request.user
        return check_user_can_upload(user, type)
