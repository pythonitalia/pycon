from files_upload.models import File
import pytest
from files_upload.tests.factories import FileFactory


@pytest.mark.parametrize(
    "type", [File.Type.PARTICIPANT_AVATAR, File.Type.PROPOSAL_RESOURCE]
)
def test_file_url(type):
    file = FileFactory(type=type)
    assert f"/files/{type}/{file.id}.txt" in file.url
