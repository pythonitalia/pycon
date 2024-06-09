from api.permissions import IsAuthenticated
from api.files_upload.types import File
from files_upload.models import File as FileModel
from api.files_upload.permissions import IsFileOwner
from files_upload.tasks import post_process_file_upload
import strawberry


@strawberry.input
class FinalizeUploadInput:
    file_id: strawberry.ID


@strawberry.mutation(
    permission_classes=[IsAuthenticated, IsFileOwner],
)
def finalize_upload(input: FinalizeUploadInput) -> File:
    post_process_file_upload.delay(input.file_id)
    return File.from_model(FileModel.objects.get(id=input.file_id))
