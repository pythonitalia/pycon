import pytest
from video_uploads.models import WetransferToS3TransferRequest
from video_uploads.tasks import process_wetransfer_to_s3_transfer_request
from video_uploads.tests.factories import WetransferToS3TransferRequestFactory

pytestmark = pytest.mark.django_db


def test_process_wetransfer_s3_request_ignores_non_queued_requests():
    request = WetransferToS3TransferRequestFactory(
        wetransfer_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=WetransferToS3TransferRequest.Status.PENDING,
    )

    process_wetransfer_to_s3_transfer_request(request.id)

    request.refresh_from_db()

    assert request.status == WetransferToS3TransferRequest.Status.PENDING


def test_process_wetransfer_s3_request_reports_exceptions(mocker):
    mocker.patch(
        "video_uploads.transfer.WetransferProcessing.run",
        side_effect=Exception("Fake exception"),
    )

    request = WetransferToS3TransferRequestFactory(
        wetransfer_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=WetransferToS3TransferRequest.Status.QUEUED,
    )

    process_wetransfer_to_s3_transfer_request(request.id)

    request.refresh_from_db()

    assert request.status == WetransferToS3TransferRequest.Status.FAILED
    assert request.failed_reason == "Fake exception"


def test_process_wetransfer_s3_request_copies_imported_files_on_success(mocker):
    mocker.patch(
        "video_uploads.transfer.WetransferProcessing.run",
        return_value=[
            "fake-download-link.txt",
            "fake-download-link-2.txt",
        ],
    )

    request = WetransferToS3TransferRequestFactory(
        wetransfer_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=WetransferToS3TransferRequest.Status.QUEUED,
    )

    process_wetransfer_to_s3_transfer_request(request.id)

    request.refresh_from_db()

    assert request.status == WetransferToS3TransferRequest.Status.DONE
    assert not request.failed_reason
    assert request.imported_files == [
        "fake-download-link.txt",
        "fake-download-link-2.txt",
    ]
    assert request.finished_at
