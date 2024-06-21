from django.urls import reverse

from files_upload.tests.factories import FileFactory


def test_local_file_upload_is_disabled_on_prod(client, settings):
    settings.DEBUG = False
    response = client.post(reverse("local_files_upload", args=[1]))

    assert response.status_code == 400


def test_local_files_upload(client, settings):
    file = FileFactory()
    settings.DEBUG = True
    response = client.post(
        reverse("local_files_upload", args=[file.id]),
        data={"file": file.file},
    )

    assert response.status_code == 204
