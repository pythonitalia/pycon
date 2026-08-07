import pytest
from conferences.tests.factories import ConferenceFactory
from video_uploads.models import VideosImportRequest
from video_uploads.admin import (
    VideosImportRequestAdminForm,
    queue_videos_import_request,
    retry_transfer,
)
from video_uploads.tests.factories import VideosImportRequestFactory

pytestmark = pytest.mark.django_db


def test_queue_videos_import_request(mocker, django_capture_on_commit_callbacks):
    mock_process_videos_import_request = mocker.patch(
        "video_uploads.admin.process_videos_import_request"
    )
    mock_check_pending_heavy_processing_work = mocker.patch(
        "video_uploads.admin.check_pending_heavy_processing_work"
    )

    request = VideosImportRequestFactory()

    with django_capture_on_commit_callbacks(execute=True):
        queue_videos_import_request(request)

    request.refresh_from_db()

    assert request.status == VideosImportRequest.Status.QUEUED
    assert request.failed_reason == ""

    mock_process_videos_import_request.apply_async.assert_called_once_with(
        args=[request.id], queue="heavy_processing"
    )
    mock_check_pending_heavy_processing_work.delay.assert_called_once()


@pytest.mark.parametrize(
    "source_url,refused_hostname",
    [
        (
            "https://wetransfer.com.evil.example/downloads/id/hash",
            "wetransfer.com.evil.example",
        ),
        (
            "https://drive.google.com.evil.example/file/d/FILE_ID/view",
            "drive.google.com.evil.example",
        ),
        (
            "https://evil.example/wetransfer.com/downloads/id/hash",
            "evil.example",
        ),
        (
            "https://drive.google.com@evil.example/file/d/FILE_ID/view",
            "evil.example",
        ),
        (
            "https://notwetransfer.com/downloads/id/hash",
            "notwetransfer.com",
        ),
        (
            "https://drive.google.com@169.254.169.254/latest/meta-data/",
            "169.254.169.254",
        ),
    ],
)
def test_admin_form_rejects_hosts_that_only_look_like_a_provider(
    source_url, refused_hostname
):
    conference = ConferenceFactory()

    form = VideosImportRequestAdminForm(
        data={"conference": conference.id, "source_url": source_url}
    )

    assert not form.is_valid()

    (error,) = form.errors["source_url"]

    assert refused_hostname in error


def test_admin_form_accepts_wetransfer_source_url():
    conference = ConferenceFactory()

    form = VideosImportRequestAdminForm(
        data={
            "conference": conference.id,
            "source_url": "https://wetransfer.com/downloads/fake_id/fake_hash",
        }
    )

    assert form.is_valid(), form.errors


@pytest.mark.parametrize(
    "source_url",
    [
        "https://drive.google.com/file/d/FILE_ID/view",
        "https://drive.google.com/drive/folders/FOLDER_ID",
    ],
)
def test_admin_form_accepts_google_drive_source_urls(source_url):
    conference = ConferenceFactory()

    form = VideosImportRequestAdminForm(
        data={"conference": conference.id, "source_url": source_url}
    )

    assert form.is_valid(), form.errors


def test_admin_queues_a_drive_folder_import_on_the_heavy_queue(
    mocker, django_capture_on_commit_callbacks
):
    mock_process_videos_import_request = mocker.patch(
        "video_uploads.admin.process_videos_import_request"
    )
    mocker.patch("video_uploads.admin.check_pending_heavy_processing_work")

    request = VideosImportRequestFactory(
        source_url="https://drive.google.com/drive/folders/FOLDER_ID"
    )

    with django_capture_on_commit_callbacks(execute=True):
        queue_videos_import_request(request)

    request.refresh_from_db()

    assert request.status == VideosImportRequest.Status.QUEUED
    mock_process_videos_import_request.apply_async.assert_called_once_with(
        args=[request.id], queue="heavy_processing"
    )


def test_admin_add_view_accepts_wetransfer_source_url(admin_superuser, http_client):
    conference = ConferenceFactory()
    http_client.force_login(admin_superuser)

    response = http_client.post(
        "/admin/video_uploads/videosimportrequest/add/",
        {
            "conference": conference.id,
            "source_url": "https://wetransfer.com/downloads/fake_id/fake_hash",
        },
    )

    assert response.status_code == 302
    assert VideosImportRequest.objects.count() == 1


def test_retry_transfer():
    obj1, obj2 = VideosImportRequestFactory.create_batch(2)
    retry_transfer(None, None, VideosImportRequest.objects.all())

    obj1.refresh_from_db()
    obj2.refresh_from_db()

    assert obj1.status == VideosImportRequest.Status.QUEUED
    assert obj2.status == VideosImportRequest.Status.QUEUED
