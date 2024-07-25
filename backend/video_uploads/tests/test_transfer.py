from pycon.constants import GB
import pytest
from io import BytesIO
from video_uploads.models import WetransferToS3TransferRequest
from video_uploads.tests.factories import WetransferToS3TransferRequestFactory
import zipfile

from video_uploads.transfer import WetransferProcessing

pytestmark = pytest.mark.django_db


class FakeStorage:
    bucket_name: str = "test"


def test_transfer_process_with_single_file(requests_mock):
    from django.core.files.storage import storages

    storage = storages["default"]

    download_mock = requests_mock.post(
        "https://wetransfer.com/api/v4/transfers/fake_transfer_id/download",
        json={"direct_link": "https://wetransfer.com/fake-download-link.txt"},
    )
    requests_mock.head(
        "https://wetransfer.com/fake-download-link.txt",
        headers={"Content-Length": "16"},
    )
    direct_link_mock = requests_mock.get(
        "https://wetransfer.com/fake-download-link.txt", content=b"fake file content"
    )

    request = WetransferToS3TransferRequestFactory(
        wetransfer_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=WetransferToS3TransferRequest.Status.QUEUED,
    )

    process = WetransferProcessing(request)
    imported_files = process.run()

    download_req = download_mock.last_request.json()
    assert {
        "security_hash": "fake_security_code",
        "intent": "entire_transfer",
    } == download_req

    assert direct_link_mock.last_request

    out = storage.listdir(f"conference-videos/{request.conference.code}/")

    assert len(out[1]) == 1
    assert out[1][0] == "fake-download-link.txt"

    assert imported_files == ["fake-download-link.txt"]


def test_transfer_process_with_zip(requests_mock):
    from django.core.files.storage import storages

    storage = storages["default"]

    requests_mock.post(
        "https://wetransfer.com/api/v4/transfers/fake_transfer_id/download",
        json={"direct_link": "https://wetransfer.com/fakezip.zip"},
    )

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.mkdir("folder")
        zf.mkdir("__MACOSX")

        zf.writestr("file1.txt", "This is the content of file1.")
        zf.writestr("file2.txt", "This is the content of file2.")
        zf.writestr("__MACOSX/file3.txt", "This is the content of file3.")
        zf.writestr(".DS_Store", "This is the content of .DS_Store.")
        zf.writestr("nested/file.txt", "This is the content of nested/file.txt.")

    zip_buffer.seek(0)
    content = zip_buffer.getvalue()

    direct_link_mock = requests_mock.get(
        "https://wetransfer.com/fakezip.zip", content=content
    )
    requests_mock.head(
        "https://wetransfer.com/fakezip.zip",
        headers={"Content-Length": str(len(content))},
    )

    request = WetransferToS3TransferRequestFactory(
        wetransfer_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=WetransferToS3TransferRequest.Status.QUEUED,
    )

    process = WetransferProcessing(request)
    imported_files = process.run()

    assert direct_link_mock.last_request

    out = storage.listdir(f"conference-videos/{request.conference.code}/")
    out_nested = storage.listdir(f"conference-videos/{request.conference.code}/nested")

    assert out[0] == ["nested"]
    assert set(out[1]) == {"file1.txt", "file2.txt"}
    assert out_nested[1] == ["file.txt"]
    assert set(imported_files) == {"file1.txt", "file2.txt", "nested/file.txt"}


def test_transfer_process_fails_with_expired_link(requests_mock):
    requests_mock.post(
        "https://wetransfer.com/api/v4/transfers/fake_transfer_id/download",
        json={},
        status_code=403,
    )

    request = WetransferToS3TransferRequestFactory(
        wetransfer_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=WetransferToS3TransferRequest.Status.QUEUED,
    )

    process = WetransferProcessing(request)
    with pytest.raises(Exception) as exc:
        process.run()

    assert str(exc.value) == "Wetransfer download link expired"


def test_transfer_determinate_num_parts_rules():
    process = WetransferProcessing(WetransferToS3TransferRequestFactory())
    assert process._determinate_total_num_of_parts(1) == 1
    assert process._determinate_total_num_of_parts(10 * GB) == 4
    assert process._determinate_total_num_of_parts(50 * GB) == 8
    assert process._determinate_total_num_of_parts(100 * GB) == 8


def test_transfer_process_via_s3_and_multi_parts(requests_mock, mocker):
    mocker.patch(
        "video_uploads.transfer.storages", return_value={"default": FakeStorage()}
    )
    mocker.patch("video_uploads.transfer.is_s3_storage", return_value=True)
    mock_boto3 = mocker.patch("video_uploads.transfer.boto3")
    mock_subprocess = mocker.patch("video_uploads.transfer.subprocess")

    download_mock = requests_mock.post(
        "https://wetransfer.com/api/v4/transfers/fake_transfer_id/download",
        json={"direct_link": "https://wetransfer.com/fake-download-link.txt"},
    )
    requests_mock.head(
        "https://wetransfer.com/fake-download-link.txt",
        headers={"Content-Length": str(500 * GB)},
    )
    direct_link_mock = requests_mock.get(
        "https://wetransfer.com/fake-download-link.txt", content=b"fake file content"
    )

    request = WetransferToS3TransferRequestFactory(
        wetransfer_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=WetransferToS3TransferRequest.Status.QUEUED,
    )

    process = WetransferProcessing(request)
    imported_files = process.run()

    download_req = download_mock.last_request.json()
    assert {
        "security_hash": "fake_security_code",
        "intent": "entire_transfer",
    } == download_req

    assert direct_link_mock.last_request
    assert imported_files == ["fake-download-link.txt"]
    subprocess_call_args = mock_subprocess.run.mock_calls[0][1][0]
    assert subprocess_call_args[0] == "cat"
    mock_boto3.client.return_value.upload_fileobj.assert_called()
    upload_mock_call_args = mock_boto3.client.return_value.upload_fileobj.mock_calls[0][
        1
    ]
    assert (
        upload_mock_call_args[2]
        == f"conference-videos/{request.conference.code}/fake-download-link.txt"
    )
