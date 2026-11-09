import pytest
from django.contrib.admin.sites import AdminSite

from files_upload.admin import FileAdmin
from files_upload.models import File
from files_upload.tests.factories import FileFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_search_files_by_uploader_email(rf, admin_superuser):
    file = FileFactory(uploaded_by=UserFactory(email="uploader@example.org"))
    FileFactory(uploaded_by=UserFactory(email="someone@example.org"))
    request = rf.get("/")
    request.user = admin_superuser

    results, _ = FileAdmin(File, AdminSite()).get_search_results(
        request, File.objects.all(), "uploader@"
    )

    assert list(results) == [file]
