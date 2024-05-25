from typing import Annotated
from uuid import uuid4
from files_upload.upload import check_user_can_upload
from files_upload.models import File, get_upload_to
from strawberry.schema_directives import OneOf
from api.context import Info
from api.permissions import IsAuthenticated
import strawberry


@strawberry.input
class ProposalResourceInput:
    proposal_id: strawberry.ID

    @property
    def purpose(self) -> File.Purpose:
        return File.Purpose.PROPOSAL_RESOURCE


@strawberry.input
class ParticipantAvatarInput:
    conference_code: str

    @property
    def purpose(self) -> File.Purpose:
        return File.Purpose.PARTICIPANT_AVATAR


@strawberry.input(directives=[OneOf])
class UploadFileInput:
    proposal_resource: ProposalResourceInput | None = strawberry.UNSET
    participant_avatar: ParticipantAvatarInput | None = strawberry.UNSET


@strawberry.type
class UploadNotAllowed:
    message: str


@strawberry.type
class FileUploadRequest:
    id: strawberry.ID
    upload_url: str
    fields: str


UploadFileOutput = Annotated[
    FileUploadRequest | UploadNotAllowed, strawberry.union(name="UploadFileOutput")
]


@strawberry.mutation(permission_classes=[IsAuthenticated])
def upload_file(info: Info, input: UploadFileInput) -> UploadFileOutput:
    user = info.context.request.user
    input_obj = input.proposal_resource or input.participant_avatar
    purpose = input_obj.purpose

    if not check_user_can_upload(user, purpose):
        return False

    id = uuid4()
    file = File.objects.create(
        id=id,
        file=get_upload_to(purpose, id),
        uploaded_by=user,
        purpose=purpose,
    )

    upload_url = file.create_upload_url()
    return FileUploadRequest(
        id=file.id,
        upload_url=upload_url.url,
        fields=upload_url.fields_as_json,
    )
