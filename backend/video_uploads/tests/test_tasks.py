import pytest
from io import BytesIO
from video_uploads.models import WetransferToS3TransferRequest
from video_uploads.tasks import process_wetransfer_to_s3_transfer_request
from video_uploads.tests.factories import WetransferToS3TransferRequestFactory
import zipfile

pytestmark = pytest.mark.django_db


def test_process_wetransfer_s3_request_ignores_non_queued_requests(requests_mock):
    download_mock = requests_mock.post(
        "https://wetransfer.com/api/v4/transfers/fake_transfer_id/download",
        json={"direct_link": "https://wetransfer.com/fake-download-link.txt"},
    )
    direct_link_mock = requests_mock.get(
        "https://wetransfer.com/fake-download-link.txt", content=b"fake file content"
    )

    request = WetransferToS3TransferRequestFactory(
        wetransfer_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=WetransferToS3TransferRequest.Status.PENDING,
    )

    process_wetransfer_to_s3_transfer_request(request.id)
    assert not download_mock.last_request
    assert not direct_link_mock.last_request

    request.refresh_from_db()

    assert request.status == WetransferToS3TransferRequest.Status.PENDING


def test_process_wetransfer_s3_request_with_single_file(requests_mock):
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

    process_wetransfer_to_s3_transfer_request(request.id)
    download_req = download_mock.last_request.json()
    assert {
        "security_hash": "fake_security_code",
        "intent": "entire_transfer",
    } == download_req

    assert direct_link_mock.last_request

    out = storage.listdir(f"conference-videos/{request.conference.code}/")

    assert len(out[1]) == 1
    assert out[1][0] == "fake-download-link.txt"

    request.refresh_from_db()

    assert request.status == WetransferToS3TransferRequest.Status.DONE
    assert request.finished_at
    assert request.imported_files == ["fake-download-link.txt"]
    assert request.failed_reason is None


def test_process_wetransfer_s3_request_with_zip(requests_mock, mocker):
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

    process_wetransfer_to_s3_transfer_request(request.id)
    assert direct_link_mock.last_request

    out = storage.listdir(f"conference-videos/{request.conference.code}/")
    out_nested = storage.listdir(f"conference-videos/{request.conference.code}/nested")

    assert out[0] == ["nested"]
    assert set(out[1]) == {"file1.txt", "file2.txt"}
    assert out_nested[1] == ["file.txt"]

    request.refresh_from_db()

    assert request.status == WetransferToS3TransferRequest.Status.DONE
    assert request.finished_at
    assert request.imported_files == ["file1.txt", "file2.txt", "nested/file.txt"]
    assert not request.failed_reason


def test_process_wetransfer_s3_request_fails_with_expired_link(requests_mock):
    requests_mock.post(
        "https://wetransfer.com/api/v4/transfers/fake_transfer_id/download",
        json={},
        status_code=403,
    )

    request = WetransferToS3TransferRequestFactory(
        wetransfer_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=WetransferToS3TransferRequest.Status.QUEUED,
    )

    process_wetransfer_to_s3_transfer_request(request.id)

    request.refresh_from_db()

    assert request.status == WetransferToS3TransferRequest.Status.FAILED
    assert request.imported_files is None
    assert request.failed_reason == "Wetransfer download link expired"
