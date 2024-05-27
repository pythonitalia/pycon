from typing import Annotated
from uuid import uuid4
from api.files_upload.permissions import IsFileTypeUploadAllowed
from api.extensions import RateLimit
from files_upload.models import File, get_upload_to
from api.context import Info
from api.permissions import IsAuthenticated
import strawberry


@strawberry.input
class BaseInput:
    filename: str


@strawberry.input
class ProposalResourceInput(BaseInput):
    proposal_id: strawberry.ID
    conference_code: str

    @property
    def type(self) -> File.Type:
        return File.Type.PROPOSAL_RESOURCE


@strawberry.input
class ParticipantAvatarInput(BaseInput):
    conference_code: str

    @property
    def type(self) -> File.Type:
        return File.Type.PARTICIPANT_AVATAR


@strawberry.input(one_of=True)
class UploadFileInput:
    proposal_resource: ProposalResourceInput | None = strawberry.UNSET
    participant_avatar: ParticipantAvatarInput | None = strawberry.UNSET

    @property
    def data(self):
        return self.proposal_resource or self.participant_avatar

    @property
    def type(self) -> File.Type:
        return self.data.type


@strawberry.type
class FileUploadRequest:
    id: strawberry.ID
    upload_url: str
    fields: str


UploadFileOutput = Annotated[
    FileUploadRequest, strawberry.union(name="UploadFileOutput")
]


@strawberry.mutation(
    permission_classes=[IsAuthenticated, IsFileTypeUploadAllowed],
    extensions=[RateLimit("10/m")],
)
def upload_file(info: Info, input: UploadFileInput) -> UploadFileOutput:
    user = info.context.request.user
    data = input.data
    type = data.type
    filename = data.filename

    id = uuid4()
    file = File.objects.create(
        id=id,
        file=get_upload_to(type, id, filename),
        uploaded_by=user,
        type=type,
    )

    upload_url = file.create_upload_url()
    return FileUploadRequest(
        id=file.id,
        upload_url=upload_url.url,
        fields=upload_url.fields_as_json,
    )
