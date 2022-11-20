from azure.storage.blob import BlobServiceClient

from blob.config import get_account_key, get_account_url
from blob.enum import BlobContainer
from blob.url_parsing import parse_azure_storage_url, verify_azure_storage_url


def confirm_blob_upload_usage(temporary_upload_url: str, blob_name: str) -> str:
    if not verify_azure_storage_url(
        url=temporary_upload_url, allowed_containers=[BlobContainer.TEMPORARY_UPLOADS]
    ):
        raise ValueError("Invalid temporary url")

    parsed_url = parse_azure_storage_url(temporary_upload_url)

    destination_container = parsed_url.paths[0]

    blob_service = BlobServiceClient(
        account_url=get_account_url(), credential=get_account_key()
    )

    copied_blob = blob_service.get_blob_client(destination_container, blob_name)
    copied_blob.start_copy_from_url(temporary_upload_url)

    temporary_blob = blob_service.get_blob_client(
        BlobContainer.TEMPORARY_UPLOADS.value, parsed_url.path
    )
    temporary_blob.delete_blob()
    return copied_blob.url
