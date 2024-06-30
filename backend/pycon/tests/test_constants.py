from files_upload.constants import get_max_upload_size_bytes
from files_upload.models import File


def test_participant_avatar_max_5mb():
    assert get_max_upload_size_bytes(File.Type.PARTICIPANT_AVATAR) == 5 * 1024 * 1024


def test_proposal_material_max_10mb():
    assert get_max_upload_size_bytes(File.Type.PROPOSAL_MATERIAL) == 10 * 1024 * 1024
