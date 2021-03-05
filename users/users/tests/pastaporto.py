from datetime import datetime, timedelta

import jwt

from users.domain import entities
from users.settings import PASTAPORTO_SECRET


def fake_pastaporto_token_for_user(user: entities.User):
    # fix me
    user._authenticated_user = True
    return jwt.encode(
        {
            "userInfo": {"id": user.id, "email": user.email},
            "credentials": user.credentials.scopes,
            "exp": datetime.now() + timedelta(minutes=1),
        },
        str(PASTAPORTO_SECRET),
        algorithm="HS256",
    )
