from api.files_upload.mutations.upload_file import upload_file
from strawberry.tools import create_type


FilesUploadMutation = create_type("FilesUploadMutation", [upload_file])
