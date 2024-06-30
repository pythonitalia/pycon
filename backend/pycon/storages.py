import json
from dataclasses import dataclass
from files_upload.constants import get_max_upload_size_bytes
import boto3
from storages.backends.s3boto3 import S3Boto3Storage
from tempfile import SpooledTemporaryFile
from storages.backends.azure_storage import AzureStorage
from django.core.files.storage.memory import InMemoryStorage
from django.core.files.storage import FileSystemStorage
from django.urls import reverse


@dataclass
class UploadURL:
    url: str
    fields: dict
    is_public: bool

    @property
    def fields_as_json(self) -> str:
        fields = self.fields.copy()

        if self.is_public:
            fields["acl"] = "public-read"

        return json.dumps(fields)


class CustomS3Boto3Storage(S3Boto3Storage):
    is_remote = True

    def generate_upload_url(self, file_obj):
        file = file_obj.file
        bucket_name = self.bucket_name
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.security_token,
            region_name=self.region_name,
            endpoint_url=f"https://s3.{self.region_name}.amazonaws.com",
        )

        conditions = [
            ["content-length-range", 1, get_max_upload_size_bytes(file_obj.type)],
        ]

        if file_obj.is_public:
            conditions.append({"acl": "public-read"})

        response = s3_client.generate_presigned_post(
            Bucket=bucket_name,
            Key=file.name,
            ExpiresIn=3600,
            Conditions=conditions,
        )

        return UploadURL(
            url=response["url"],
            fields=response["fields"],
            is_public=file_obj.is_public,
        )

    def url(
        self,
        name,
        *,
        parameters=None,
        expire=None,
        http_method=None,
        querystring_auth=True,
    ):
        # todo find a better workaround?
        old_value = self.querystring_auth

        if not querystring_auth:
            self.querystring_auth = False

        try:
            return super().url(
                name=name, parameters=parameters, expire=expire, http_method=http_method
            )
        finally:
            self.querystring_auth = old_value

    def _save(self, name, content):
        content.seek(0)
        with SpooledTemporaryFile() as tmp:
            tmp.write(content.read())
            return super()._save(name, tmp)


class CustomInMemoryStorage(InMemoryStorage):
    is_remote = False

    def generate_upload_url(self, file_obj):
        return UploadURL(
            url=f"memory://{file_obj.file.name}",
            fields={"in-memory": True},
            is_public=False,
        )

    def url(self, name, *, querystring_auth=True):
        return super().url(name)


class ConferenceVideosStorage(AzureStorage):
    azure_container = "conference-videos"


class CustomFileSystemStorage(FileSystemStorage):
    is_remote = False

    def generate_upload_url(self, file_obj):
        url = reverse("local_files_upload", kwargs={"file_id": file_obj.id})
        return UploadURL(url=url, fields={}, is_public=False)

    def url(self, name, *, querystring_auth=True):
        return super().url(name)
