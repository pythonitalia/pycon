from blob.enum import BlobContainer
from blob.url_parsing import parse_azure_storage_url, verify_azure_storage_url


def test_verify_azure_storage_url(settings):
    settings.AZURE_STORAGE_ACCOUNT_NAME = "pytest-fakestorageaccount"

    assert (
        verify_azure_storage_url(
            url="https://pytest-fakestorageaccount.blob.core.windows.net/participants-avatars/my-photo.jpg",
            allowed_containers=[
                BlobContainer.PARTICIPANTS_AVATARS,
            ],
        )
        is True
    )

    assert (
        verify_azure_storage_url(
            url="https://pytest-fakestorageaccount.blob.core.windows.net/temporary-uploads/my-photo.jpg",
            allowed_containers=[BlobContainer.PARTICIPANTS_AVATARS],
        )
        is False
    )


def test_verify_azure_storage_url_with_multiple_containers(settings):
    settings.AZURE_STORAGE_ACCOUNT_NAME = "pytest-fakestorageaccount"

    assert (
        verify_azure_storage_url(
            url="https://pytest-fakestorageaccount.blob.core.windows.net/temporary-uploads/my-photo.jpg",
            allowed_containers=[
                BlobContainer.PARTICIPANTS_AVATARS,
                BlobContainer.TEMPORARY_UPLOADS,
            ],
        )
        is True
    )


def test_verify_azure_storage_url_different_account(settings):
    settings.AZURE_STORAGE_ACCOUNT_NAME = "accountaccount"

    assert (
        verify_azure_storage_url(
            url="https://pytest-fakestorageaccount.blob.core.windows.net/participants-avatars/my-photo.jpg",
            allowed_containers=[BlobContainer.PARTICIPANTS_AVATARS],
        )
        is False
    )


def test_parse_azure_storage_url():
    url = "https://pytest-fakestorageaccount.blob.core.windows.net/participants-avatars/my-photo.jpg"
    parsed_url = parse_azure_storage_url(url)

    assert parsed_url.account == "pytest-fakestorageaccount"
    assert parsed_url.container == BlobContainer.PARTICIPANTS_AVATARS
    assert parsed_url.paths == ["my-photo.jpg"]


def test_parse_azure_storage_url_multiple_paths():
    url = "https://pytest-fakestorageaccount.blob.core.windows.net/participants-avatars/another/path/my-photo.jpg"
    parsed_url = parse_azure_storage_url(url)

    assert parsed_url.account == "pytest-fakestorageaccount"
    assert parsed_url.container == BlobContainer.PARTICIPANTS_AVATARS
    assert parsed_url.paths == ["another", "path", "my-photo.jpg"]


def test_parse_azure_storage_url_with_wrong_url():
    url = "https://pytest-fakestorageaccount.windows.net/participants-avatars/another/path/my-photo.jpg"
    parsed_url = parse_azure_storage_url(url)

    assert parsed_url is None
