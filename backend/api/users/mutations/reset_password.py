from django.db.models import F
from users.models import User as UserModel
from django.utils.functional import cached_property
import jwt
import strawberry
from django.conf import settings
from api.types import BaseErrorType
from api.users.types import OperationSuccess
import logging

logger = logging.getLogger(__file__)


@strawberry.type
class ResetPasswordErrors(BaseErrorType):
    token: list[str] = strawberry.field(default_factory=list)
    new_password: list[str] = strawberry.field(default_factory=list)


@strawberry.input
class ResetPasswordInput:
    token: str
    new_password: str

    @cached_property
    def decoded_token(self):
        return jwt.decode(
            self.token,
            str(settings.SECRET_KEY),
            issuer="pycon-backend",
            audience="pycon-backend/reset-password",
            algorithms=["HS256"],
            options={"require": ["exp", "iss", "aud", "iat", "jti"]},
        )

    def validate(self):
        errors = ResetPasswordErrors()

        if not self.token:
            errors.add_error("token", "Token is required")

        if not self.new_password:
            errors.add_error("new_password", "New password is required")

        if len(self.new_password) < 8:
            errors.add_error("new_password", "Password must be at least 8 characters")

        try:
            self.decode_token
        except jwt.ExpiredSignatureError:
            errors.add_error("token", "Token has expired")
        except (jwt.InvalidAudienceError, jwt.MissingRequiredClaimError):
            errors.add_error("token", "Invalid token")

        return errors.if_has_errors


ResetPasswordResult = strawberry.union(
    "ResetPasswordResult", (ResetPasswordErrors, OperationSuccess)
)


@strawberry.mutation
def reset_password(input: ResetPasswordInput) -> ResetPasswordResult:
    if validation_result := input.validate():
        return validation_result

    decoded_token = input.decoded_token

    user = UserModel.objects.filter(id=decoded_token["user_id"]).first()

    if not user or not user.is_active:
        return OperationSuccess(ok=False)

    if decoded_token["jti"] != user.jwt_auth_id:
        return ResetPasswordErrors.with_error("token", "Invalid token")

    logger.info("Resetting password of user_id=%s", user.id)

    user.set_password(input.new_password)
    user.jwt_auth_id = F("jwt_auth_id") + 1
    user.save()
    return OperationSuccess(ok=True)
