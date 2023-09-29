from api.permissions import IsAuthenticated
from api.context import Info
from datetime import date
from typing import Optional
import strawberry

from api.types import BaseErrorType
from api.users.types import User


@strawberry.type
class UpdateProfileErrors(BaseErrorType):
    name: list[str] = strawberry.field(default_factory=list)
    full_name: list[str] = strawberry.field(default_factory=list)
    gender: list[str] = strawberry.field(default_factory=list)
    open_to_recruiting: list[str] = strawberry.field(default_factory=list)
    open_to_newsletter: list[str] = strawberry.field(default_factory=list)
    date_birth: list[str] = strawberry.field(default_factory=list)
    country: list[str] = strawberry.field(default_factory=list)


@strawberry.input
class UpdateProfileInput:
    name: str
    full_name: str
    gender: str
    open_to_recruiting: bool
    open_to_newsletter: bool
    date_birth: Optional[date]
    country: str

    def validate(self):
        errors = UpdateProfileErrors()

        required_fields = [
            "name",
            "full_name",
            "gender",
            "open_to_recruiting",
            "open_to_newsletter",
            "date_birth",
            "country",
        ]

        for field in required_fields:
            if not getattr(self, field):
                errors.add_error(field, f"{field} is required")

        return errors.if_has_errors


UpdateProfileResult = strawberry.union(
    "UpdateProfileResult", (UpdateProfileErrors, User)
)


@strawberry.mutation(permission_classes=[IsAuthenticated])
def update_profile(info: Info, input: UpdateProfileInput) -> UpdateProfileResult:
    if validation_result := input.validate():
        return validation_result

    user = info.context.request.user
    user.name = input.name
    user.full_name = input.full_name
    user.gender = input.gender
    user.open_to_recruiting = input.open_to_recruiting
    user.open_to_newsletter = input.open_to_newsletter
    user.date_birth = input.date_birth
    user.country = input.country
    user.save(
        update_fields=[
            "name",
            "full_name",
            "gender",
            "open_to_recruiting",
            "open_to_newsletter",
            "date_birth",
            "country",
        ]
    )

    return User.from_django_model(user)
