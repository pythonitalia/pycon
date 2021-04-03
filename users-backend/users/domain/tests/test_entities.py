from datetime import datetime, timezone

import jwt
import time_machine
from users.domain.entities import User
from users.settings import SECRET_KEY
from ward import test


@test("generate reset password token")
async def _():
    user = User(
        id=50,
        email="test@email.it",
        date_joined=datetime.now(timezone.utc),
        jwt_auth_id=1,
    )

    with time_machine.travel("2020-10-10 10:10:10Z", tick=False):
        token = user.create_reset_password_token()

        decoded_token = jwt.decode(
            token,
            str(SECRET_KEY),
            audience="users/reset-password",
            issuer="users",
            algorithms=["HS256"],
        )

    assert decoded_token["user_id"] == 50
    assert decoded_token["jti"] == "reset-password:50:1"
