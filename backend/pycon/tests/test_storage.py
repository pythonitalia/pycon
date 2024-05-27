from unittest import mock
from files_upload.tests.factories import FileFactory
from pycon.storages import CustomS3Boto3Storage


def test_s3_storage_generate_upload_url(mocker):
    boto3_mock = mocker.patch("pycon.storages.boto3.client")
    boto3_mock.return_value.generate_presigned_post.return_value = {
        "url": "http://example.org/pycon-test",
        "fields": {
            "key": "test.txt",
            "bucket": "pycon-test",
        },
    }
    file = FileFactory()
    storage = CustomS3Boto3Storage()
    return_value = storage.generate_upload_url(file.file)
    boto3_mock.return_value.generate_presigned_post.assert_called_once_with(
        Bucket=mock.ANY,
        Key=file.file.name,
        ExpiresIn=3600,
    )

    assert return_value.url == "http://example.org/pycon-test"
    assert return_value.fields == {
        "key": "test.txt",
        "bucket": "pycon-test",
    }
    assert return_value.fields_as_json == '{"key": "test.txt", "bucket": "pycon-test"}'
