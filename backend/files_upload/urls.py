from django.urls import path
from files_upload.views import local_file_upload


urlpatterns = [
    path(
        "local_files_upload/<path:file_id>",
        local_file_upload,
        name="local_files_upload",
    ),
]
