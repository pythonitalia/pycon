import json
import os

import pytest
from django.core.files.storage import default_storage
from django.test import RequestFactory

from upload.models import Upload
from upload.views import file_upload


@pytest.fixture()
def file_sample():

    path = "testfile.txt"
    f = open(path, "w")
    f.write("Hello World")
    f.close()

    post_data = {"file": open(path, "rb")}

    yield (path, post_data)

    if os.path.exists(path):
        os.remove(path)


@pytest.fixture()
def upload_file(file_sample):
    path, post_data = file_sample
    request = RequestFactory().post("upload/", data=post_data)
    resp = file_upload(request)

    yield (resp, path)

    if os.path.exists(path):
        os.remove(path)

    url = json.loads(resp.content)["url"]
    if default_storage.exists(url):
        default_storage.delete(url)


@pytest.mark.django_db
def test_file_upload(upload_file):  # Create a sample test file on the fly
    resp, path = upload_file

    assert resp.status_code == 200
    assert len(Upload.objects.all()) == 1


def test_forbitten(file_sample):

    path, post_data = file_sample
    request = RequestFactory().get("upload/", data=post_data)
    resp = file_upload(request)

    assert resp.status_code == 403
