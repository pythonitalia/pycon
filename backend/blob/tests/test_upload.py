from datetime import datetime

import time_machine

from blob.enum import BlobContainer
from blob.upload import create_blob_upload


def test_create_blob_upload(mocker, settings):
    settings.AZURE_STORAGE_ACCOUNT_NAME = "testaccount"
    settings.AZURE_STORAGE_ACCOUNT_KEY = "key"

    mock_generate_blob_sas = mocker.patch(
        "blob.upload.generate_blob_sas", return_value="se=123&token=abc"
    )

    with time_machine.travel("2022-10-10 13:00:00Z", tick=False):
        result = create_blob_upload(
            container=BlobContainer.PARTICIPANTS_AVATARS, blob_name="blobblob.jpg"
        )

    assert mock_generate_blob_sas.call_args[1]["account_name"] == "testaccount"
    assert mock_generate_blob_sas.call_args[1]["account_key"] == "key"
    assert (
        mock_generate_blob_sas.call_args[1]["blob_name"]
        == "participants-avatars/blobblob.jpg"
    )
    assert (
        mock_generate_blob_sas.call_args[1]["container_name"]
        == BlobContainer.TEMPORARY_UPLOADS.value
    )
    # expires 3 mins after
    assert mock_generate_blob_sas.call_args[1]["expiry"] == datetime(
        2022, 10, 10, 13, 3, 0
    )
    assert mock_generate_blob_sas.call_args[1]["permission"].read is False
    assert mock_generate_blob_sas.call_args[1]["permission"].write is True

    assert (
        "https://testaccount.blob.core.windows.net/temporary-uploads/participants-avatars/blobblob.jpg?se=123&token=abc"
        == result.upload_url
    )
    assert (
        "https://testaccount.blob.core.windows.net/temporary-uploads/participants-avatars/blobblob.jpg"
        == result.file_url
    )
