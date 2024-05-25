from api.files_upload.mutations.upload_file import upload_file
from strawberry.tools import create_type

from api.files_upload.mutations.generate_participant_avatar_upload_url import (
    generate_participant_avatar_upload_url,
)


FilesUploadMutation = create_type(
    "FilesUploadMutation", [generate_participant_avatar_upload_url, upload_file]
)
