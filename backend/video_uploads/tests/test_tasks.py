import pytest
from google_api.models import GoogleCloudOAuthCredential, GoogleCloudToken
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


def test_process_videos_import_request_imports_a_drive_file_end_to_end(
    requests_mock, admin_user
):
    from django.core.files.storage import storages

    credential = GoogleCloudOAuthCredential.objects.create()
    GoogleCloudToken.objects.create(
        oauth_credential=credential,
        token="stale-token",
        refresh_token="refresh-token",
        admin_user=admin_user,
    )

    content = b"drive video bytes"
    requests_mock.post(
        "https://oauth2.googleapis.com/token",
        json={
            "access_token": "drive-token",
            "expires_in": 3600,
            "token_type": "Bearer",
        },
    )
    requests_mock.get(
        "https://www.googleapis.com/drive/v3/files/FILE_ID",
        json={
            "id": "FILE_ID",
            "name": "keynote.mp4",
            "size": str(len(content)),
            "mimeType": "video/mp4",
        },
    )
    requests_mock.get(
        "https://www.googleapis.com/drive/v3/files/FILE_ID?alt=media", content=content
    )

    request = VideosImportRequestFactory(
        source_url="https://drive.google.com/file/d/FILE_ID/view",
        status=VideosImportRequest.Status.QUEUED,
    )

    process_videos_import_request(request.id)

    request.refresh_from_db()

    assert request.status == VideosImportRequest.Status.DONE
    assert request.imported_files == ["keynote.mp4"]
    assert request.started_at
    assert request.finished_at
    assert not request.failed_reason

    stored = storages["default"].listdir(
        f"conference-videos/{request.conference.code}/"
    )
    assert stored[1] == ["keynote.mp4"]


def test_process_videos_import_request_fails_readably_without_drive_credentials():
    request = VideosImportRequestFactory(
        source_url="https://drive.google.com/file/d/FILE_ID/view",
        status=VideosImportRequest.Status.QUEUED,
    )

    process_videos_import_request(request.id)

    request.refresh_from_db()

    assert request.status == VideosImportRequest.Status.FAILED
    assert "authorize" in request.failed_reason.lower()


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
