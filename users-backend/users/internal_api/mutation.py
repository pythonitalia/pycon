import logging
from typing import Optional

import strawberry

from users.domain.services.exceptions import (
    UserIsNotActiveError,
    UserIsNotAdminError,
    WrongEmailOrPasswordError,
)
from users.domain.services.login import LoginInputModel, login as login_service
from users.internal_api.context import Info
from users.internal_api.input_types import LoginInput
from users.internal_api.permissions import IsService
from users.internal_api.types import User

logger = logging.getLogger(__name__)


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsService(["pycon-backend"])])
    async def login(self, info: Info, input: LoginInput) -> Optional[User]:
        logger.info("Internal api request to login")
        try:
            logged_user = await login_service(
                input=LoginInputModel(email=input.email, password=input.password),
                reject_non_admins=input.staff_only,
                users_repository=info.context.users_repository,
            )
            return User.from_domain(logged_user)
        except (
            WrongEmailOrPasswordError,
            UserIsNotActiveError,
            UserIsNotAdminError,
        ) as e:
            logger.info("Login failed", exc_info=e)
            return None
