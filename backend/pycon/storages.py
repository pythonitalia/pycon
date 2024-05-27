import json
from dataclasses import dataclass
import boto3
from storages.backends.s3boto3 import S3Boto3Storage
from tempfile import SpooledTemporaryFile
from storages.backends.azure_storage import AzureStorage
from django.core.files.storage.memory import InMemoryStorage


@dataclass
class UploadURL:
    url: str
    fields: dict

    @property
    def fields_as_json(self) -> str:
        return json.dumps(self.fields)


class CustomS3Boto3Storage(S3Boto3Storage):
    def generate_upload_url(self, file):
        bucket_name = self.bucket_name
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
            endpoint_url=f"https://s3.{self.region_name}.amazonaws.com",
        )
        response = s3_client.generate_presigned_post(
            Bucket=bucket_name,
            Key=file.name,
            ExpiresIn=3600,
        )
        return UploadURL(
            url=response["url"],
            fields=response["fields"],
        )

    def _save(self, name, content):
        content.seek(0)
        with SpooledTemporaryFile() as tmp:
            tmp.write(content.read())
            return super()._save(name, tmp)


class CustomInMemoryStorage(InMemoryStorage):
    def generate_upload_url(self, file):
        return UploadURL(url=f"memory://{file.name}", fields={"in-memory": True})


class ConferenceVideosStorage(AzureStorage):
    azure_container = "conference-videos"
