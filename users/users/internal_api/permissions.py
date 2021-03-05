from starlette.requests import Request

from users.settings import SERVICE_KEY_X_HEADER, SERVICE_TO_SERVICE_SECRET


def is_service(request: Request) -> bool:
    key = request.headers.get(SERVICE_KEY_X_HEADER)
    return key and key == str(SERVICE_TO_SERVICE_SECRET)
