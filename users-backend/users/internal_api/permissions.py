from pythonit_toolkit.api.permissions import IsService as BaseIsService

from users.settings import SERVICE_TO_SERVICE_SECRET


def IsService(allowed_callers: list[str]):
    return BaseIsService(
        allowed_callers, str(SERVICE_TO_SERVICE_SECRET), "users-backend"
    )
