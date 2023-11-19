import pytest


pytestmark = pytest.mark.django_db


# def test_get_available_credentials():
#     credential = GoogleCloudOAuthCredential.objects.create(
#         quota_limit_for_youtube=10_000,
#     )

#     found = GoogleCloudOAuthCredential.get_available_credentials(
#         service="youtube",
#         min_quota=1600,
#     )

#     assert found.id == credential.id
