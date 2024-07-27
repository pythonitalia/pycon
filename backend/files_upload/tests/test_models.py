import pytest
from files_upload.models import File
from files_upload.tests.factories import FileFactory

mark = pytest.mark.django_db


@pytest.mark.parametrize(
    "type", [File.Type.PARTICIPANT_AVATAR, File.Type.PROPOSAL_MATERIAL]
)
def test_file_url(type):
    file = FileFactory(type=type)
    assert f"/files/{type}/{file.id}.txt" in file.url
