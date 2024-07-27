import pytest
from submissions.tests.factories import ProposalMaterialFactory
import pyclamd
import datetime
from participants.tests.factories import ParticipantFactory
from files_upload.models import File
import time_machine
from files_upload.tasks import delete_unused_files, post_process_file_upload
from files_upload.tests.factories import FileFactory
from django.utils import timezone
from django.test import override_settings
from django.core.files.storage.memory import InMemoryStorage


mark = pytest.mark.django_db


class FakeRemoteStorage(InMemoryStorage):
    is_remote = True

    def url(self, name, *args, **kwargs):
        return "http://example.org/example.txt"

    def generate_upload_url(self, file_obj):
        ...


def test_delete_unused_files():
    file_1 = FileFactory(
        created=timezone.datetime(2010, 8, 10, 10, 0, 0, tzinfo=datetime.timezone.utc),
        type=File.Type.PARTICIPANT_AVATAR,
    )

    file_2 = FileFactory(
        created=timezone.datetime(2010, 10, 10, 5, 0, 0, tzinfo=datetime.timezone.utc),
        type=File.Type.PARTICIPANT_AVATAR,
    )

    file_3 = FileFactory(
        created=timezone.datetime(2010, 1, 4, 10, 0, 0, tzinfo=datetime.timezone.utc),
        type=File.Type.PARTICIPANT_AVATAR,
    )
    ParticipantFactory(photo_file=file_3)

    file_4 = FileFactory(
        created=timezone.datetime(2009, 1, 4, 10, 0, 0, tzinfo=datetime.timezone.utc),
        type=File.Type.PROPOSAL_MATERIAL,
    )
    ProposalMaterialFactory(file=file_4)

    with time_machine.travel("2010-10-10 10:20:00Z", tick=False):
        delete_unused_files()

    assert not File.objects.filter(id=file_1.id).exists()
    assert File.objects.filter(id=file_2.id).exists()
    assert File.objects.filter(id=file_3.id).exists()
    assert File.objects.filter(id=file_4.id).exists()


def test_post_process_file_upload(requests_mock, mocker):
    file = FileFactory()

    mock_pyclamd = mocker.patch("pyclamd.ClamdNetworkSocket")
    mock_pyclamd.return_value.scan_stream.return_value = {
        file.file.path: ("FOUND", "virus type")
    }

    mock_magika = mocker.patch("magika.Magika.identify_path")
    mock_magika.return_value.output.mime_type = "text/plain"

    post_process_file_upload(file.id)

    file.refresh_from_db()

    assert file.virus
    assert file.mime_type == "text/plain"


def test_post_process_file_upload_no_virus(requests_mock, mocker):
    file = FileFactory()

    mock_pyclamd = mocker.patch("pyclamd.ClamdNetworkSocket")
    mock_pyclamd.return_value.scan_stream.return_value = {}

    mock_magika = mocker.patch("magika.Magika.identify_path")
    mock_magika.return_value.output.mime_type = "text/plain"

    post_process_file_upload(file.id)

    file.refresh_from_db()

    assert not file.virus
    assert file.mime_type == "text/plain"


def test_post_process_handles_connection_errors(mocker):
    mocker.patch("time.sleep")

    file = FileFactory()

    mock_pyclamd = mocker.patch("pyclamd.ClamdNetworkSocket")
    mock_pyclamd.side_effect = pyclamd.ConnectionError

    mock_magika = mocker.patch("magika.Magika.identify_path")
    mock_magika.return_value.output.mime_type = "text/plain"

    post_process_file_upload(file.id)

    file.refresh_from_db()

    assert file.virus is None
    assert file.mime_type == "text/plain"


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "files_upload.tests.test_tasks.FakeRemoteStorage",
        },
    }
)
def test_post_process_file_upload_remote_file(requests_mock, mocker):
    requests_mock.get("http://example.org/example.txt", content=b"test")

    file = FileFactory()

    mock_pyclamd = mocker.patch("pyclamd.ClamdNetworkSocket")
    mock_pyclamd.return_value.scan_stream.return_value = None

    mock_magika = mocker.patch("magika.Magika.identify_path")
    mock_magika.return_value.output.mime_type = "text/plain"

    post_process_file_upload(file.id)

    file.refresh_from_db()

    assert not file.virus
    assert file.mime_type == "text/plain"


def test_check_we_updated_delete_files_job():
    known_types = ["participant_avatar", "proposal_material"]
    assert (
        File.Type.values == known_types
    ), "Please update the delete_unused_files job to include new file types"
