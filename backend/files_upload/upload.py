from files_upload.models import File
from users.models import User


def check_user_can_upload(user: User, type: File.Type) -> bool:
    if not user.is_authenticated:
        return False

    match type:
        case File.Type.PARTICIPANT_AVATAR:
            return True
        case File.Type.PROPOSAL_RESOURCE:
            return True
        case _:
            return False
