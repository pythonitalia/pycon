from dataclasses import dataclass
from datetime import datetime, timedelta

from azure.storage.blob import BlobSasPermissions, generate_blob_sas

from blob.config import _build_url, get_account_key, get_account_name
from blob.enum import BlobContainer


@dataclass(frozen=True)
class BlobUpload:
    upload_url: str
    file_url: str


def create_blob_upload(container: BlobContainer, blob_name: str) -> BlobUpload:
    """Create an upload URL to let the client upload the file
    The file is first uploaded to the temporary container, and moved to the actual container
    only once it is confirmed

    Args:
        container (str): the container where the file should be moved once the usage is confirmed
        blob_name (str): the name of the blob
    """
    tmp_blob_name = f"{container.value}/{blob_name}"
    tmp_container = BlobContainer.TEMPORARY_UPLOADS.value

    sas_token = generate_blob_sas(
        account_name=get_account_name(),
        account_key=get_account_key(),
        container_name=tmp_container,
        blob_name=tmp_blob_name,
        permission=BlobSasPermissions(write=True),
        expiry=datetime.utcnow() + timedelta(minutes=3),
    )

    return BlobUpload(
        upload_url=_build_url(
            container=tmp_container,
            blob=tmp_blob_name,
            sas_token=sas_token,
        ),
        file_url=_build_url(
            container=tmp_container,
            blob=tmp_blob_name,
        ),
    )
