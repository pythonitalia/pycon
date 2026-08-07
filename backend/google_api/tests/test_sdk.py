import datetime
from unittest import mock
import time_machine
from google_api.models import (
    GoogleCloudOAuthCredential,
    GoogleCloudToken,
    UsedRequestQuota,
)
from google_api.exceptions import NoGoogleCloudQuotaLeftError
from google_api.sdk import (
    count_quota,
    drive_file_metadata,
    drive_list_files_in_folder,
    get_available_credentials,
    get_drive_credentials,
    youtube_videos_insert,
    youtube_videos_set_thumbnail,
)
import pytest

pytestmark = pytest.mark.django_db

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


@pytest.fixture
def drive_credential(admin_user):
    stored_credential = GoogleCloudOAuthCredential.objects.create()
    GoogleCloudToken.objects.create(
        oauth_credential=stored_credential,
        token="stale-token",
        refresh_token="refresh-token",
        admin_user=admin_user,
    )
    return stored_credential


def mock_token_refresh(requests_mock):
    return requests_mock.post(
        GOOGLE_TOKEN_URL,
        json={
            "access_token": "refreshed-token",
            "expires_in": 3600,
            "token_type": "Bearer",
        },
    )


def test_get_drive_credentials_refreshes_the_stored_token(
    requests_mock, drive_credential
):
    mock_token_refresh(requests_mock)

    credentials = get_drive_credentials()

    assert credentials.token == "refreshed-token"


def test_drive_file_metadata_sends_the_refreshed_bearer_token(
    requests_mock, drive_credential
):
    mock_token_refresh(requests_mock)
    metadata_mock = requests_mock.get(
        "https://www.googleapis.com/drive/v3/files/file123",
        json={
            "id": "file123",
            "name": "talk.mp4",
            "size": "1024",
            "mimeType": "video/mp4",
        },
    )

    metadata = drive_file_metadata(file_id="file123")

    assert metadata["name"] == "talk.mp4"
    assert (
        metadata_mock.last_request.headers["Authorization"] == "Bearer refreshed-token"
    )
    assert metadata_mock.last_request.qs["supportsalldrives"] == ["true"]
    assert drive_credential.usedrequestquota_set.filter(service="drive").count() == 1


def test_drive_list_files_in_folder_follows_pagination(requests_mock, drive_credential):
    mock_token_refresh(requests_mock)
    requests_mock.get(
        "https://www.googleapis.com/drive/v3/files",
        [
            {
                "json": {
                    "files": [{"id": "1", "name": "a.mp4", "mimeType": "video/mp4"}],
                    "nextPageToken": "page-2",
                }
            },
            {
                "json": {
                    "files": [{"id": "2", "name": "b.mp4", "mimeType": "video/mp4"}]
                }
            },
        ],
    )

    files = list(drive_list_files_in_folder(folder_id="folder123"))

    assert [file["id"] for file in files] == ["1", "2"]


def test_drive_list_files_in_folder_queries_only_the_folder_children(
    requests_mock, drive_credential
):
    mock_token_refresh(requests_mock)
    listing_mock = requests_mock.get(
        "https://www.googleapis.com/drive/v3/files", json={"files": []}
    )

    list(drive_list_files_in_folder(folder_id="folder123"))

    query = listing_mock.last_request.qs["q"][0]
    assert "'folder123' in parents" in query
    assert "trashed = false" in query


def test_drive_helpers_fail_when_no_credential_has_drive_quota(admin_user):
    stored_credential = GoogleCloudOAuthCredential.objects.create(
        quota_limit_for_drive=0
    )
    GoogleCloudToken.objects.create(
        oauth_credential=stored_credential, token="token", admin_user=admin_user
    )

    with pytest.raises(NoGoogleCloudQuotaLeftError):
        drive_file_metadata(file_id="file123")


def test_get_available_credentials(admin_user):
    stored_credential = GoogleCloudOAuthCredential.objects.create()
    GoogleCloudToken.objects.create(
        oauth_credential=stored_credential, token="token", admin_user=admin_user
    )

    available_credentials = get_available_credentials("youtube", 1000)

    assert available_credentials.token == "token"


def test_get_available_credentials_fails_when_no_quota_is_left(admin_user):
    stored_credential = GoogleCloudOAuthCredential.objects.create(
        quota_limit_for_youtube=500
    )
    GoogleCloudToken.objects.create(
        oauth_credential=stored_credential, token="token", admin_user=admin_user
    )

    with pytest.raises(NoGoogleCloudQuotaLeftError):
        get_available_credentials("youtube", 1000)


def test_count_quota(admin_user):
    stored_credential = GoogleCloudOAuthCredential.objects.create()
    GoogleCloudToken.objects.create(
        oauth_credential=stored_credential, token="token", admin_user=admin_user
    )

    @count_quota("youtube", 1000)
    def test_function(*, credentials):
        return credentials

    with time_machine.travel("2023-10-10 12:00:00", tick=False):
        credentials = test_function()

        assert credentials.token == "token"
        assert stored_credential.usedrequestquota_set.count() == 1

        used_quota = stored_credential.usedrequestquota_set.first()
        assert used_quota.cost == 1000
        assert used_quota.service == "youtube"
        assert used_quota.used_at == datetime.datetime.now(tz=datetime.timezone.utc)


def test_count_quota_with_generator_function(admin_user):
    stored_credential = GoogleCloudOAuthCredential.objects.create()
    GoogleCloudToken.objects.create(
        oauth_credential=stored_credential, token="token", admin_user=admin_user
    )

    @count_quota("youtube", 1000)
    def test_generator_function(*, credentials):
        yield 1
        yield 2
        yield 3

    with time_machine.travel("2023-10-20 12:00:00", tick=False):
        generator = test_generator_function()
        vals = []

        for val in generator:
            vals.append(val)

        assert vals == [1, 2, 3]

        assert stored_credential.usedrequestquota_set.count() == 1

        used_quota = stored_credential.usedrequestquota_set.first()
        assert used_quota.cost == 1000
        assert used_quota.service == "youtube"
        assert used_quota.used_at == datetime.datetime.now(tz=datetime.timezone.utc)


def test_youtube_videos_insert(mocker, admin_user):
    stored_credential = GoogleCloudOAuthCredential.objects.create()
    GoogleCloudToken.objects.create(
        oauth_credential=stored_credential, token="token", admin_user=admin_user
    )

    mock_build = mocker.patch("google_api.sdk.build")
    mocker.patch("google_api.sdk.MediaFileUpload")

    mock_youtube = mocker.Mock()
    mock_build.return_value = mock_youtube

    mock_upload_request = mocker.Mock()
    mock_youtube.videos.return_value.insert.return_value = mock_upload_request
    mock_upload_request.next_chunk.side_effect = [(None, {"id": "12345"})]

    response = list(
        youtube_videos_insert(
            title="Title",
            description="Description",
            tags="Tag1,Tag2",
            file_path="/file/test.mp4",
        )
    )

    mock_build.assert_called_with("youtube", "v3", credentials=mocker.ANY)

    mock_youtube.videos.return_value.insert.assert_called_with(
        part="snippet,status",
        notifySubscribers=False,
        body={
            "snippet": {
                "title": "Title",
                "description": "Description",
                "tags": "Tag1,Tag2",
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=mock.ANY,
    )

    assert response[0] is None
    assert response[1]["id"] == "12345"

    assert UsedRequestQuota.objects.filter(service="youtube", cost=1600).exists()


def test_youtube_videos_insert_when_failing_raises_an_error(mocker, admin_user):
    stored_credential = GoogleCloudOAuthCredential.objects.create()
    GoogleCloudToken.objects.create(
        oauth_credential=stored_credential, token="token", admin_user=admin_user
    )

    mock_build = mocker.patch("google_api.sdk.build")
    mocker.patch("google_api.sdk.MediaFileUpload")

    mock_youtube = mocker.Mock()
    mock_build.return_value = mock_youtube

    mock_upload_request = mocker.Mock()
    mock_youtube.videos.return_value.insert.return_value = mock_upload_request
    mock_upload_request.next_chunk.side_effect = [(None, {"error": "Message"})]

    with pytest.raises(ValueError) as exc:
        list(
            youtube_videos_insert(
                title="Title",
                description="Description",
                tags="Tag1,Tag2",
                file_path="/file/test.mp4",
            )
        )

    assert "The upload failed with an unexpected response: {'error': 'Message'}" == str(
        exc.value
    )

    mock_youtube.videos.return_value.insert.assert_called_with(
        part="snippet,status",
        notifySubscribers=False,
        body={
            "snippet": {
                "title": "Title",
                "description": "Description",
                "tags": "Tag1,Tag2",
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=mock.ANY,
    )

    assert UsedRequestQuota.objects.filter(service="youtube", cost=1600).exists()


def test_youtube_videos_set_thumbnail(mocker, admin_user):
    stored_credential = GoogleCloudOAuthCredential.objects.create()
    GoogleCloudToken.objects.create(
        oauth_credential=stored_credential, token="token", admin_user=admin_user
    )

    mock_build = mocker.patch("google_api.sdk.build")
    mocker.patch("google_api.sdk.MediaFileUpload")

    mock_youtube = mocker.Mock()
    mock_build.return_value = mock_youtube

    mock_youtube.thumbnails.return_value.set.return_value.execute.return_value = {}

    youtube_videos_set_thumbnail(video_id="123", thumbnail_path="/test.png")

    mock_build.assert_called_with("youtube", "v3", credentials=mocker.ANY)

    mock_youtube.thumbnails.return_value.set.assert_called_once_with(
        videoId="123", media_body=mock.ANY
    )

    assert UsedRequestQuota.objects.filter(service="youtube", cost=50).exists()
