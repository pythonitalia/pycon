from api.files_upload.mutations.upload_file import upload_file
from api.files_upload.mutations.finalize_upload import finalize_upload
from strawberry.tools import create_type


FilesUploadMutation = create_type("FilesUploadMutation", [upload_file, finalize_upload])
