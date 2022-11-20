from unittest.mock import call

import pytest

from blob.confirmation import confirm_blob_upload_usage


def test_confirm_blob_upload_usage(mocker, settings):
    settings.AZURE_STORAGE_ACCOUNT_NAME = "pytest-fakestorageaccount"
    mock_client = mocker.patch("blob.confirmation.BlobServiceClient")

    url = "https://pytest-fakestorageaccount.blob.core.windows.net/temporary-uploads/participants-avatars/my-photo.jpg"

    confirm_blob_upload_usage(temporary_upload_url=url, blob_name="my-photo.jpg")

    mock_client().get_blob_client.assert_has_calls(
        [
            # copy file to the container
            call("participants-avatars", "my-photo.jpg"),
            call().start_copy_from_url(url),
            # delete temporary file
            call("temporary-uploads", "participants-avatars/my-photo.jpg"),
            call().delete_blob(),
        ]
    )


def test_confirm_blob_upload_usage_with_different_name(mocker, settings):
    settings.AZURE_STORAGE_ACCOUNT_NAME = "pytest-fakestorageaccount"
    mock_client = mocker.patch("blob.confirmation.BlobServiceClient")

    url = "https://pytest-fakestorageaccount.blob.core.windows.net/temporary-uploads/participants-avatars/another-name"

    confirm_blob_upload_usage(
        temporary_upload_url=url, blob_name="different-name/my-photo.jpg"
    )

    mock_client().get_blob_client.assert_has_calls(
        [
            # copy file to the container
            call("participants-avatars", "different-name/my-photo.jpg"),
            call().start_copy_from_url(url),
            # delete temporary file
            call("temporary-uploads", "participants-avatars/another-name"),
            call().delete_blob(),
        ]
    )


def test_confirm_blob_upload_usage_only_accepts_temporary_uploads_files(settings):
    settings.AZURE_STORAGE_ACCOUNT_NAME = "pytest-fakestorageaccount"

    url = "https://pytest-fakestorageaccount.blob.core.windows.net/participants-avatars/participants-avatars/my-photo.jpg"
    with pytest.raises(ValueError, match="Invalid temporary url"):
        confirm_blob_upload_usage(temporary_upload_url=url, blob_name="name.jpg")
