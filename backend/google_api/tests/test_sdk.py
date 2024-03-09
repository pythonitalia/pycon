import datetime
import time_machine
from google_api.models import GoogleCloudOAuthCredential, GoogleCloudToken
from google_api.exceptions import NoGoogleCloudQuotaLeftError
from google_api.sdk import count_quota, get_available_credentials
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
