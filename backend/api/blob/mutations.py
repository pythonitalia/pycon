from uuid import uuid4

import strawberry
from strawberry.types import Info

from api.permissions import IsAuthenticated
from blob.enum import BlobContainer
from blob.upload import create_blob_upload


@strawberry.type
class AvatarUploadUrl:
    upload_url: str
    file_url: str


@strawberry.field(permission_classes=[IsAuthenticated])
def generate_participant_avatar_upload_url(info: Info) -> AvatarUploadUrl:
    blob_name = f"{uuid4()}.jpg"
    blob_upload = create_blob_upload(BlobContainer.PARTICIPANTS_AVATARS, blob_name)

    return AvatarUploadUrl(
        upload_url=blob_upload.upload_url,
        file_url=blob_upload.file_url,
    )
