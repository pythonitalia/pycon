import pydantic
import strawberry
from pythonit_toolkit.api.builder import create_validation_error_type
from pythonit_toolkit.api.permissions import IsAuthenticated
from pythonit_toolkit.api.types import PydanticError

from users.api.context import Info
from users.api.types import User
from users.domain.services.update_profile import (
    UpdateProfileInput as UpdateProfileInputModel,
)
from users.domain.services.update_profile import (
    update_profile as service_update_profile,
)


@strawberry.experimental.pydantic.input(
    UpdateProfileInputModel,
    fields=[
        "name",
        "full_name",
        "gender",
        "open_to_recruiting",
        "open_to_newsletter",
        "date_birth",
        "country",
        "tagline",
    ],
)
class UpdateProfileInput:
    pass


@strawberry.type
class UpdateProfileErrors:
    name: PydanticError = None
    full_name: PydanticError = None
    gender: PydanticError = None
    open_to_recruiting: PydanticError = None
    open_to_newsletter: PydanticError = None
    date_birth: PydanticError = None
    country: PydanticError = None
    tagline: PydanticError = None


UpdateProfileValidationError = create_validation_error_type(
    "UpdateProfile", UpdateProfileErrors
)


UpdateProfileResult = strawberry.union(
    "UpdateProfileResult", (User, UpdateProfileValidationError)
)


@strawberry.mutation(permission_classes=[IsAuthenticated])
async def update_profile(input: UpdateProfileInput, info: Info) -> UpdateProfileResult:
    try:
        input_model = input.to_pydantic()
    except pydantic.ValidationError as exc:
        return UpdateProfileValidationError.from_validation_error(exc)

    user = await service_update_profile(
        int(info.context.request.user.id),
        input_model,
        users_repository=info.context.users_repository,
    )
    return User.from_domain(user)
