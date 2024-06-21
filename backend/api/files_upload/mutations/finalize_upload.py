from api.permissions import IsAuthenticated
from api.files_upload.types import File
from files_upload.models import File as FileModel
from api.files_upload.permissions import IsFileOwner
from files_upload.tasks import post_process_file_upload
import strawberry
from celery.exceptions import TimeoutError


@strawberry.input
class FinalizeUploadInput:
    file_id: strawberry.ID


@strawberry.mutation(
    permission_classes=[IsAuthenticated, IsFileOwner],
)
def finalize_upload(input: FinalizeUploadInput) -> File:
    file = FileModel.objects.filter(id=input.file_id).first()

    if file.virus is None:
        task = post_process_file_upload.delay(input.file_id)

        try:
            task.get(timeout=60)
        except TimeoutError:
            pass

        file.refresh_from_db()

    return File.from_django(file)
