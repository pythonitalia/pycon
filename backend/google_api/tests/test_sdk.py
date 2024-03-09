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
    get_available_credentials,
    youtube_videos_insert,
    youtube_videos_set_thumbnail,
)
import pytest

pytestmark = pytest.mark.django_db


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

    mock_youtube.thumbnails.return_value.set.assert_called_once_with(
        videoId="123", media_body=mock.ANY
    )

    assert UsedRequestQuota.objects.filter(service="youtube", cost=50).exists()
