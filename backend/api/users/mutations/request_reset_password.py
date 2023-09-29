import strawberry
from django.utils import timezone
from datetime import timedelta
from api.users.types import OperationSuccess
from users.models import User as UserModel
from pythonit_toolkit.emails.templates import EmailTemplate
from pythonit_toolkit.emails import get_email_backend
from django.conf import settings
import jwt
import logging

logger = logging.getLogger(__file__)
RequestResetPasswordResult = strawberry.union(
    "RequestResetPasswordResult", (OperationSuccess,)
)


@strawberry.mutation
def request_reset_password(email: str) -> RequestResetPasswordResult:
    if not email:
        return OperationSuccess(ok=False)

    user = UserModel.objects.filter(email=email).first()

    if not user or not user.is_active:
        return OperationSuccess(ok=False)

    token = _create_reset_password_token(user=user)

    backend = get_email_backend(
        settings.PYTHONIT_EMAIL_BACKEND, environment=settings.ENVIRONMENT
    )
    backend.send_email(
        template=EmailTemplate.RESET_PASSWORD,
        from_=settings.DEFAULT_EMAIL_FROM,
        to=user.email,
        subject="Reset your password",
        variables={
            "firstname": user.name,
            "resetpasswordlink": f"https://pycon.it/reset-password/{token}",
        },
    )
    logger.info("Sent reset password token to user_id=%s", user.id)
    return OperationSuccess(ok=True)


def _create_reset_password_token(user: UserModel) -> str:
    now = timezone.now()

    return jwt.encode(
        {
            "jti": f"reset-password:{user.id}:{user.jwt_auth_id}",
            "user_id": user.id,
            "exp": now + timedelta(hours=1),
            "iat": now,
            "iss": "pycon-backend",
            "aud": "pycon-backend/reset-password",
        },
        str(settings.SECRET_KEY),
        algorithm="HS256",
    )
