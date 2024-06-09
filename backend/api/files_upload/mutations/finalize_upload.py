from api.permissions import IsAuthenticated
from api.files_upload.types import File
import strawberry


@strawberry.input
class FinalizeUploadInput:
    file_id: strawberry.ID


@strawberry.mutation(
    permission_classes=[IsAuthenticated],
)
def finalize_upload(input: FinalizeUploadInput) -> File:
    pass
