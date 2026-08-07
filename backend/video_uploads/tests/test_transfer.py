import logging
from pycon.constants import GB, MB
import pytest
from io import BytesIO
from video_uploads.models import VideosImportRequest
from video_uploads.tests.factories import VideosImportRequestFactory
import zipfile

from google_api.models import GoogleCloudOAuthCredential, GoogleCloudToken
from video_uploads.transfer import (
    DriveResourceKind,
    GoogleDriveProcessing,
    UnsupportedVideoImportUrlError,
    WetransferProcessing,
    get_processing_class,
    parse_drive_url,
)

pytestmark = pytest.mark.django_db


class FakeStorage:
    bucket_name: str = "test"


def test_transfer_process_with_single_file(requests_mock):
    from django.core.files.storage import storages

    storage = storages["default"]

    content = b"fake file content"

    download_mock = requests_mock.post(
        "https://wetransfer.com/api/v4/transfers/fake_transfer_id/download",
        json={"direct_link": "https://wetransfer.com/fake-download-link.txt"},
    )
    requests_mock.head(
        "https://wetransfer.com/fake-download-link.txt",
        headers={"Content-Length": str(len(content))},
    )
    direct_link_mock = requests_mock.get(
        "https://wetransfer.com/fake-download-link.txt", content=content
    )

    request = VideosImportRequestFactory(
        source_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=VideosImportRequest.Status.QUEUED,
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

    request = VideosImportRequestFactory(
        source_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=VideosImportRequest.Status.QUEUED,
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

    request = VideosImportRequestFactory(
        source_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=VideosImportRequest.Status.QUEUED,
    )

    process = WetransferProcessing(request)
    with pytest.raises(Exception) as exc:
        process.run()

    assert str(exc.value) == "Wetransfer download link expired"


def test_transfer_determinate_num_parts_rules():
    process = WetransferProcessing(VideosImportRequestFactory())
    assert process._determinate_total_num_of_parts(1) == 1
    assert process._determinate_total_num_of_parts(10 * GB) == 4
    assert process._determinate_total_num_of_parts(50 * GB) == 8
    assert process._determinate_total_num_of_parts(100 * GB) == 8


def test_transfer_determine_parts_info():
    process = WetransferProcessing(VideosImportRequestFactory())
    parts = process.determine_parts_info(100 * MB)

    assert len(parts) == 1
    assert parts[0].byte_start == 0
    assert parts[0].byte_end == 100 * MB
    assert parts[0].part_number == 1

    parts = process.determine_parts_info(10 * GB)

    assert len(parts) == 4
    assert parts[0].byte_start == 0
    assert parts[0].byte_end == 2.5 * GB
    assert parts[0].part_number == 1

    assert parts[1].byte_start == 2.5 * GB
    assert parts[1].byte_end == 5 * GB
    assert parts[1].part_number == 2

    assert parts[2].byte_start == 5 * GB
    assert parts[2].byte_end == 7.5 * GB
    assert parts[2].part_number == 3

    assert parts[3].byte_start == 7.5 * GB
    assert parts[3].byte_end == 10 * GB
    assert parts[3].part_number == 4


def test_transfer_cleanup():
    process = WetransferProcessing(VideosImportRequestFactory())
    process.cleanup()


def test_transfer_process_via_s3_and_multi_parts(requests_mock, mocker):
    mock_getsize = mocker.patch("video_uploads.transfer.os.path.getsize")
    mock_getsize.return_value = 500 * GB / 8

    mock_storages = mocker.patch("video_uploads.transfer.storages")
    mock_storages.__getitem__.return_value.bucket_name = "bucket-name"
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

    request = VideosImportRequestFactory(
        source_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=VideosImportRequest.Status.QUEUED,
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
    assert upload_mock_call_args[1] == "bucket-name"
    assert (
        upload_mock_call_args[2]
        == f"conference-videos/{request.conference.code}/fake-download-link.txt"
    )


DRIVE_TOKEN_URL = "https://oauth2.googleapis.com/token"
DRIVE_FILES_URL = "https://www.googleapis.com/drive/v3/files"


@pytest.fixture
def drive_credential(admin_user):
    credential = GoogleCloudOAuthCredential.objects.create()
    GoogleCloudToken.objects.create(
        oauth_credential=credential,
        token="stale-token",
        refresh_token="refresh-token",
        admin_user=admin_user,
    )
    return credential


def mock_drive_auth(requests_mock):
    requests_mock.post(
        DRIVE_TOKEN_URL,
        json={
            "access_token": "drive-token",
            "expires_in": 3600,
            "token_type": "Bearer",
        },
    )


def test_drive_imports_a_single_file(requests_mock, drive_credential):
    from django.core.files.storage import storages

    storage = storages["default"]
    content = b"fake drive video"

    mock_drive_auth(requests_mock)
    requests_mock.get(
        f"{DRIVE_FILES_URL}/FILE_ID",
        json={
            "id": "FILE_ID",
            "name": "talk.mp4",
            "size": str(len(content)),
            "mimeType": "video/mp4",
        },
    )
    media_mock = requests_mock.get(
        f"{DRIVE_FILES_URL}/FILE_ID?alt=media", content=content
    )

    request = VideosImportRequestFactory(
        source_url="https://drive.google.com/file/d/FILE_ID/view",
        status=VideosImportRequest.Status.QUEUED,
    )

    imported_files = GoogleDriveProcessing(request).run()

    assert imported_files == ["talk.mp4"]
    assert media_mock.last_request.headers["Authorization"] == "Bearer drive-token"

    out = storage.listdir(f"conference-videos/{request.conference.code}/")
    assert out[1] == ["talk.mp4"]


def test_drive_unzips_a_zip_file(requests_mock, drive_credential):
    from django.core.files.storage import storages

    storage = storages["default"]

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.mkdir("__MACOSX")
        zf.writestr("file1.txt", "content of file1")
        zf.writestr("__MACOSX/file3.txt", "junk")
        zf.writestr(".DS_Store", "junk")
        zf.writestr("nested/file.txt", "content of nested")

    content = zip_buffer.getvalue()

    mock_drive_auth(requests_mock)
    requests_mock.get(
        f"{DRIVE_FILES_URL}/ZIP_ID",
        json={
            "id": "ZIP_ID",
            "name": "videos.zip",
            "size": str(len(content)),
            "mimeType": "application/zip",
        },
    )
    requests_mock.get(f"{DRIVE_FILES_URL}/ZIP_ID?alt=media", content=content)

    request = VideosImportRequestFactory(
        source_url="https://drive.google.com/file/d/ZIP_ID/view",
        status=VideosImportRequest.Status.QUEUED,
    )

    imported_files = GoogleDriveProcessing(request).run()

    assert set(imported_files) == {"file1.txt", "nested/file.txt"}

    out = storage.listdir(f"conference-videos/{request.conference.code}/")
    assert out[1] == ["file1.txt"]


def test_drive_downloads_large_files_in_ranged_parts(
    requests_mock, mocker, drive_credential
):
    mock_getsize = mocker.patch("video_uploads.transfer.os.path.getsize")
    mock_getsize.return_value = 500 * GB / 8

    mock_storages = mocker.patch("video_uploads.transfer.storages")
    mock_storages.__getitem__.return_value.bucket_name = "bucket-name"
    mocker.patch("video_uploads.transfer.is_s3_storage", return_value=True)
    mocker.patch("video_uploads.transfer.boto3")
    mocker.patch("video_uploads.transfer.subprocess")

    mock_drive_auth(requests_mock)
    requests_mock.get(
        f"{DRIVE_FILES_URL}/BIG_ID",
        json={
            "id": "BIG_ID",
            "name": "big.mp4",
            "size": str(500 * GB),
            "mimeType": "video/mp4",
        },
    )
    requests_mock.get(f"{DRIVE_FILES_URL}/BIG_ID?alt=media", content=b"chunk")

    request = VideosImportRequestFactory(
        source_url="https://drive.google.com/file/d/BIG_ID/view",
        status=VideosImportRequest.Status.QUEUED,
    )

    GoogleDriveProcessing(request).run()

    media_requests = [
        sent
        for sent in requests_mock.request_history
        if sent.qs.get("alt") == ["media"]
    ]

    assert len(media_requests) == 8
    for sent in media_requests:
        assert sent.headers["Range"].startswith("bytes=")
        assert sent.headers["Authorization"] == "Bearer drive-token"


DRIVE_FOLDER_MIME = "application/vnd.google-apps.folder"


def mock_drive_folder_listing(requests_mock, pages_by_folder_id):
    """Answer the Drive listing endpoint based on the folder named in ?q= ."""
    # requests_mock lowercases parsed query strings, so match on that.
    pages_by_folder_id = {
        folder_id.lower(): pages for folder_id, pages in pages_by_folder_id.items()
    }

    def listing(request, context):
        query = request.qs["q"][0]
        folder_id = query.split("'")[1]
        pages = pages_by_folder_id[folder_id]
        page_token = request.qs.get("pagetoken", [None])[0]
        page_index = 0 if page_token is None else int(page_token)

        payload = {"files": pages[page_index]}
        if page_index + 1 < len(pages):
            payload["nextPageToken"] = str(page_index + 1)

        return payload

    return requests_mock.get(DRIVE_FILES_URL, json=listing)


def test_drive_imports_a_folder_recursively(requests_mock, drive_credential, caplog):
    from django.core.files.storage import storages

    storage = storages["default"]
    caplog.set_level(logging.INFO, logger="video_uploads.transfer")

    mock_drive_auth(requests_mock)
    mock_drive_folder_listing(
        requests_mock,
        {
            "FOLDER_ID": [
                # first page
                [
                    {
                        "id": "F1",
                        "name": "keynote.mp4",
                        "mimeType": "video/mp4",
                        "size": "5",
                    },
                    {"id": "SUB", "name": "day2", "mimeType": DRIVE_FOLDER_MIME},
                ],
                # second page, reached through nextPageToken
                [
                    {
                        "id": "F2",
                        "name": "lightning.mp4",
                        "mimeType": "video/mp4",
                        "size": "5",
                    },
                    {
                        "id": "DOC",
                        "name": "Running order",
                        "mimeType": "application/vnd.google-apps.document",
                    },
                    {
                        "id": "LINK",
                        "name": "shortcut to talk",
                        "mimeType": "application/vnd.google-apps.shortcut",
                    },
                ],
            ],
            "SUB": [
                [
                    {
                        "id": "F3",
                        "name": "closing.mp4",
                        "mimeType": "video/mp4",
                        "size": "5",
                    }
                ]
            ],
        },
    )

    for file_id in ["F1", "F2", "F3"]:
        requests_mock.get(f"{DRIVE_FILES_URL}/{file_id}?alt=media", content=b"video")

    request = VideosImportRequestFactory(
        source_url="https://drive.google.com/drive/folders/FOLDER_ID",
        status=VideosImportRequest.Status.QUEUED,
    )

    imported_files = GoogleDriveProcessing(request).run()

    assert set(imported_files) == {
        "keynote.mp4",
        "lightning.mp4",
        "day2/closing.mp4",
    }

    conference_code = request.conference.code
    out = storage.listdir(f"conference-videos/{conference_code}/")
    assert set(out[1]) == {"keynote.mp4", "lightning.mp4"}

    nested = storage.listdir(f"conference-videos/{conference_code}/day2")
    assert nested[1] == ["closing.mp4"]

    skipped = [
        record.getMessage() for record in caplog.records if "Skipping" in record.message
    ]
    assert len(skipped) == 2
    assert any("Running order" in message for message in skipped)
    assert any("shortcut to talk" in message for message in skipped)


def test_drive_imports_an_empty_folder(requests_mock, drive_credential):
    mock_drive_auth(requests_mock)
    mock_drive_folder_listing(requests_mock, {"EMPTY_ID": [[]]})

    request = VideosImportRequestFactory(
        source_url="https://drive.google.com/drive/folders/EMPTY_ID",
        status=VideosImportRequest.Status.QUEUED,
    )

    assert GoogleDriveProcessing(request).run() == []


def test_drive_refuses_to_import_a_google_native_file(requests_mock, drive_credential):
    mock_drive_auth(requests_mock)
    requests_mock.get(
        f"{DRIVE_FILES_URL}/DOC_ID",
        json={
            "id": "DOC_ID",
            "name": "Notes",
            "mimeType": "application/vnd.google-apps.document",
        },
    )

    request = VideosImportRequestFactory(
        source_url="https://drive.google.com/file/d/DOC_ID/view",
        status=VideosImportRequest.Status.QUEUED,
    )

    with pytest.raises(Exception) as exc:
        GoogleDriveProcessing(request).run()

    assert "Google-native" in str(exc.value)


def test_get_processing_class_selects_google_drive_for_drive_urls():
    assert (
        get_processing_class("https://drive.google.com/file/d/FILE_ID/view")
        is GoogleDriveProcessing
    )


@pytest.mark.parametrize(
    "url,expected_id",
    [
        ("https://drive.google.com/file/d/FILE_ID/view", "FILE_ID"),
        ("https://drive.google.com/file/d/FILE_ID/view?usp=sharing", "FILE_ID"),
        ("https://drive.google.com/file/d/FILE_ID/edit", "FILE_ID"),
        ("https://drive.google.com/file/d/FILE_ID", "FILE_ID"),
        ("https://drive.google.com/open?id=FILE_ID", "FILE_ID"),
    ],
)
def test_parse_drive_url_reads_file_links(url, expected_id):
    resource = parse_drive_url(url)

    assert resource.kind == DriveResourceKind.FILE
    assert resource.id == expected_id


@pytest.mark.parametrize(
    "url,expected_id",
    [
        ("https://drive.google.com/drive/folders/FOLDER_ID", "FOLDER_ID"),
        ("https://drive.google.com/drive/folders/FOLDER_ID?usp=sharing", "FOLDER_ID"),
        ("https://drive.google.com/drive/u/0/folders/FOLDER_ID", "FOLDER_ID"),
    ],
)
def test_parse_drive_url_reads_folder_links(url, expected_id):
    resource = parse_drive_url(url)

    assert resource.kind == DriveResourceKind.FOLDER
    assert resource.id == expected_id


@pytest.mark.parametrize(
    "url",
    [
        "https://drive.google.com/",
        "https://drive.google.com/file/d/",
        "https://drive.google.com/open",
        "https://example.com/file/d/FILE_ID/view",
    ],
)
def test_parse_drive_url_rejects_unrecognised_links(url):
    with pytest.raises(UnsupportedVideoImportUrlError):
        parse_drive_url(url)


def test_get_processing_class_selects_wetransfer_for_wetransfer_urls():
    assert (
        get_processing_class(
            "https://wetransfer.com/downloads/fake_transfer_id/fake_security_code"
        )
        is WetransferProcessing
    )


def test_get_processing_class_rejects_unsupported_urls():
    with pytest.raises(UnsupportedVideoImportUrlError) as exc:
        get_processing_class("https://example.com/some-video.mp4")

    assert "example.com" in str(exc.value)


def test_wetransfer_download_sends_no_authorization_header(requests_mock):
    content = b"fake file content"

    requests_mock.post(
        "https://wetransfer.com/api/v4/transfers/fake_transfer_id/download",
        json={"direct_link": "https://wetransfer.com/fake-download-link.txt"},
    )
    requests_mock.head(
        "https://wetransfer.com/fake-download-link.txt",
        headers={"Content-Length": str(len(content))},
    )
    requests_mock.get("https://wetransfer.com/fake-download-link.txt", content=content)

    request = VideosImportRequestFactory(
        source_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=VideosImportRequest.Status.QUEUED,
    )

    WetransferProcessing(request).run()

    assert requests_mock.request_history
    for sent_request in requests_mock.request_history:
        assert "Authorization" not in sent_request.headers


def test_transfer_process_retries_downloading_parts(requests_mock, mocker):
    mock_getsize = mocker.patch("video_uploads.transfer.os.path.getsize")
    mock_getsize.return_value = 100

    mock_storages = mocker.patch("video_uploads.transfer.storages")
    mock_storages.__getitem__.return_value.bucket_name = "bucket-name"
    mocker.patch("video_uploads.transfer.is_s3_storage", return_value=True)
    mocker.patch("video_uploads.transfer.boto3")
    mocker.patch("video_uploads.transfer.subprocess")

    requests_mock.post(
        "https://wetransfer.com/api/v4/transfers/fake_transfer_id/download",
        json={"direct_link": "https://wetransfer.com/fake-download-link.txt"},
    )
    requests_mock.head(
        "https://wetransfer.com/fake-download-link.txt",
        headers={"Content-Length": str(500 * GB)},
    )
    requests_mock.get(
        "https://wetransfer.com/fake-download-link.txt", content=b"fake file content"
    )

    request = VideosImportRequestFactory(
        source_url="https://wetransfer.com/downloads/fake_transfer_id/fake_security_code",
        status=VideosImportRequest.Status.QUEUED,
    )

    process = WetransferProcessing(request)
    with pytest.raises(Exception) as exc:
        process.run()

    assert "Failed to download part" in str(exc.value)
