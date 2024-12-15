import json
from dataclasses import dataclass
from files_upload.constants import get_max_upload_size_bytes
import boto3
from storages.backends.s3boto3 import S3Boto3Storage
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


class PrivateCustomS3Boto3Storage(CustomS3Boto3Storage):
    default_acl = "private"

    def get_object_parameters(self, name):
        params = super().get_object_parameters(name)
        params.pop("CacheControl", None)
        return params


class CustomInMemoryStorage(InMemoryStorage):
    is_remote = False

    def generate_upload_url(self, file_obj):
        return UploadURL(
            url=f"memory://{file_obj.file.name}",
            fields={"in-memory": True},
            is_public=False,
        )


class CustomFileSystemStorage(FileSystemStorage):
    is_remote = False

    def generate_upload_url(self, file_obj):
        url = reverse("local_files_upload", kwargs={"file_id": file_obj.id})
        return UploadURL(url=url, fields={}, is_public=False)
