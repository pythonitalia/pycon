from django.urls import path
from upload.views import file_upload

urlpatterns = [path("upload", file_upload)]
