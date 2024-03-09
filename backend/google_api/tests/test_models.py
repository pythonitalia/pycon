import time_machine
from google_api.models import GoogleCloudOAuthCredential, UsedRequestQuota
import pytest


pytestmark = pytest.mark.django_db


def test_with_quota_left():
    credential = GoogleCloudOAuthCredential.objects.create(
        quota_limit_for_youtube=10_000,
    )

    with time_machine.travel("2023-10-10 00:00:00", tick=False):
        result = GoogleCloudOAuthCredential.objects.with_quota_left("youtube").get()
        assert result.youtube_quota_left == 10_000

        UsedRequestQuota.objects.create(
            credentials=credential,
            cost=1000,
            service="youtube",
        )

        result = GoogleCloudOAuthCredential.objects.with_quota_left("youtube").get()
        assert result.youtube_quota_left == 9_000

    with time_machine.travel("2023-10-10 08:00:00", tick=False):
        result = GoogleCloudOAuthCredential.objects.with_quota_left("youtube").get()
        assert result.youtube_quota_left == 10_000


def test_get_by_client_id():
    credential = GoogleCloudOAuthCredential.objects.create(client_id="test123")

    assert (
        GoogleCloudOAuthCredential.objects.get_by_client_id("test123").id
        == credential.id
    )
    assert GoogleCloudOAuthCredential.objects.get_by_client_id("invalid") is None
