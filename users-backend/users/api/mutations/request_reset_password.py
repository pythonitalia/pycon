import logging

import strawberry

from users.api.context import Info
from users.api.types import OperationSuccess
from users.domain import services
from users.domain.services.exceptions import UserIsNotActiveError

logger = logging.getLogger(__file__)

RequestResetPasswordResult = strawberry.union(
    "RequestResetPasswordResult", (OperationSuccess,)
)


@strawberry.mutation
async def request_reset_password(info: Info, email: str) -> RequestResetPasswordResult:
    user = await info.context.users_repository.get_by_email(email)

    if not user:
        logger.info("Trying to request reset password of not existent user")
        return OperationSuccess(ok=True)

    try:
        await services.request_reset_password(user)
    except UserIsNotActiveError:
        pass

    return OperationSuccess(ok=True)
