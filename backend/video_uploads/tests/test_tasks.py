import pytest
from video_uploads.models import VideosImportRequest
from video_uploads.tasks import process_videos_import_request
from video_uploads.tests.factories import VideosImportRequestFactory

pytestmark = pytest.mark.django_db


def test_process_videos_import_request_ignores_non_queued_requests():
    request = VideosImportRequestFactory(
        source_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=VideosImportRequest.Status.PENDING,
    )

    process_videos_import_request(request.id)

    request.refresh_from_db()

    assert request.status == VideosImportRequest.Status.PENDING


def test_process_videos_import_request_reports_exceptions(mocker):
    mocker.patch(
        "video_uploads.transfer.WetransferProcessing.run",
        side_effect=Exception("Fake exception"),
    )

    request = VideosImportRequestFactory(
        source_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=VideosImportRequest.Status.QUEUED,
    )

    process_videos_import_request(request.id)

    request.refresh_from_db()

    assert request.status == VideosImportRequest.Status.FAILED
    assert request.failed_reason == "Fake exception"


def test_process_videos_import_request_copies_imported_files_on_success(mocker):
    mocker.patch(
        "video_uploads.transfer.WetransferProcessing.run",
        return_value=[
            "fake-download-link.txt",
            "fake-download-link-2.txt",
        ],
    )

    request = VideosImportRequestFactory(
        source_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=VideosImportRequest.Status.QUEUED,
    )

    process_videos_import_request(request.id)

    request.refresh_from_db()

    assert request.status == VideosImportRequest.Status.DONE
    assert not request.failed_reason
    assert request.imported_files == [
        "fake-download-link.txt",
        "fake-download-link-2.txt",
    ]
    assert request.finished_at
