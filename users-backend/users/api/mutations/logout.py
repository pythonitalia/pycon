import strawberry

from users.api.context import Info
from users.settings import ENVIRONMENT, IDENTITY_COOKIE_KEY


@strawberry.mutation
def logout(info: Info) -> str:
    info.context.response.set_cookie(
        key=IDENTITY_COOKIE_KEY,
        value="invalid",
        max_age=-1,
        httponly=True,
        secure=ENVIRONMENT != "local",
        samesite="strict",
    )
    return "ok"
