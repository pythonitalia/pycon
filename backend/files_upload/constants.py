from files_upload.models import File


MAX_UPLOAD_SIZES_IN_MB = {
    File.Type.PARTICIPANT_AVATAR: 5,
    File.Type.PROPOSAL_MATERIAL: 10,
}


def get_max_upload_size_bytes(file_type: File.Type) -> int:
    return MAX_UPLOAD_SIZES_IN_MB[file_type] * 1024 * 1024
