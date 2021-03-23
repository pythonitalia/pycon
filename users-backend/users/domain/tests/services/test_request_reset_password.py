from datetime import datetime

from users.domain.entities import User
from users.domain.services.exceptions import UserIsNotActiveError
from users.domain.services.request_reset_password import request_reset_password
from ward import raises, test


@test("test request reset password")
async def _():
    user = User(email="test@email.it", date_joined=datetime.utcnow(), is_active=True)
    await request_reset_password(user)

    # assert email sent?


@test("cannot request reset password of not active user")
async def _():
    user = User(email="test@email.it", date_joined=datetime.utcnow(), is_active=False)
    with raises(UserIsNotActiveError):
        await request_reset_password(user)
