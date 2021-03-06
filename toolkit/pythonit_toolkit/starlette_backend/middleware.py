from pythonit_toolkit.starlette_backend.pastaporto_backend import (
    PastaportoAuthBackend,
    on_auth_error,
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware


def pastaporto_auth_middleware(secret: str):
    return Middleware(
        AuthenticationMiddleware,
        backend=PastaportoAuthBackend(secret),
        on_error=on_auth_error,
    )
