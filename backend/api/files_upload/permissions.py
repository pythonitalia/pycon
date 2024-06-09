from typing import TYPE_CHECKING

from conferences.models.conference import Conference
from submissions.models import Submission
from files_upload.models import File
from strawberry.permission import BasePermission

if TYPE_CHECKING:
    from api.files_upload.mutations.upload_file import UploadFileInput
    from api.files_upload.mutations.finalize_upload import FinalizeUploadInput


class IsFileTypeUploadAllowed(BasePermission):
    message = "You cannot upload files of this type"

    def has_permission(self, source, info, input: "UploadFileInput", **kwargs):
        type = input.type
        user = info.context.request.user

        assert type in File.Type.values, f"Invalid file type: {type}"

        match type:
            case File.Type.PARTICIPANT_AVATAR:
                return self._check_participant_avatar(user, input)
            case File.Type.PROPOSAL_RESOURCE:
                return self._check_proposal_resource(user, input)

    def _check_participant_avatar(self, user, input: "UploadFileInput") -> bool:
        conference_code = input.data.conference_code
        return Conference.objects.filter(code=conference_code).exists()

    def _check_proposal_resource(self, user, input: "UploadFileInput") -> bool:
        proposal_id = input.data.proposal_id
        conference_code = input.data.conference_code

        try:
            proposal = Submission.objects.for_conference_code(
                conference_code
            ).get_by_hashid(proposal_id)
        except (Submission.DoesNotExist, IndexError):
            return False

        return proposal.speaker_id == user.id


class IsFileOwner(BasePermission):
    message = "File not found"

    def has_permission(self, source, info, input: "FinalizeUploadInput", **kwargs):
        user = info.context.request.user
        file_id = input.file_id
        file = File.objects.filter(id=file_id).first()

        if not file:
            return False

        return file.uploaded_by_id == user.id
