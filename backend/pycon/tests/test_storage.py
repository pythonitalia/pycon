from unittest import mock
from files_upload.models import File
from files_upload.tests.factories import FileFactory
from pycon.storages import (
    CustomFileSystemStorage,
    CustomS3Boto3Storage,
    PrivateCustomS3Boto3Storage,
)


def test_s3_storage_generate_public_upload_url(mocker):
    boto3_mock = mocker.patch("pycon.storages.boto3.client")
    boto3_mock.return_value.generate_presigned_post.return_value = {
        "url": "http://example.org/pycon-test",
        "fields": {
            "key": "test.txt",
            "bucket": "pycon-test",
        },
    }
    file = FileFactory(type=File.Type.PARTICIPANT_AVATAR)
    storage = CustomS3Boto3Storage()
    return_value = storage.generate_upload_url(file)
    boto3_mock.return_value.generate_presigned_post.assert_called_once_with(
        Bucket=mock.ANY,
        Key=file.file.name,
        ExpiresIn=3600,
        Conditions=[["content-length-range", 1, 5242880], {"acl": "public-read"}],
    )

    assert return_value.url == "http://example.org/pycon-test"
    assert return_value.fields == {
        "key": "test.txt",
        "bucket": "pycon-test",
    }
    assert (
        return_value.fields_as_json
        == '{"key": "test.txt", "bucket": "pycon-test", "acl": "public-read"}'
    )


def test_local_storage_generate_upload_url():
    file = FileFactory()
    storage = CustomFileSystemStorage()
    return_value = storage.generate_upload_url(file)
    assert f"local_files_upload/{file.id}" in return_value.url
    assert return_value.fields == {}
    assert return_value.fields_as_json == "{}"


def test_private_storage_removes_cache_control_params():
    storage = PrivateCustomS3Boto3Storage()
    params = storage.get_object_parameters("test.pdf")
    assert "CacheControl" not in params
