import json
import os

import pytest

from django.test import RequestFactory, override_settings
from upload.models import File
from upload.views import file_upload


def _file_sample():

    path = "testfile.txt"
    f = open(path, "w")
    f.write("Hello World")
    f.close()

    post_data = {"file": open(path, "rb")}

    return path, post_data


@pytest.fixture()
def upload_file():
    path, post_data = _file_sample()
    request = RequestFactory().post("upload/", data=post_data)
    resp = file_upload(request)

    yield (resp, path)

    if os.path.exists(path):
        return os.remove(path)


@pytest.mark.django_db
@override_settings(MEDIA_ROOT="/tmp/django_test")
def test_file_upload(upload_file):  # Create a sample test file on the fly
    resp, path = upload_file
    content = json.loads(resp.content)

    assert resp.status_code == 200
    assert len(File.objects.all()) == 1
    assert os.path.exists(content["url"])


def test_forbitten():

    path, post_data = _file_sample()
    request = RequestFactory().get("upload/", data=post_data)
    resp = file_upload(request)

    assert resp.status_code == 403
