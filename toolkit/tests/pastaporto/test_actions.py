from calendar import timegm
from datetime import datetime, timedelta

import jwt
import time_machine
from pythonit_toolkit.pastaporto.actions import (
    Action,
    PastaportoAction,
    create_user_auth_pastaporto_action,
)
from ward import test


@test("create user auth action")
async def _():
    action = create_user_auth_pastaporto_action(10)
    assert action.action == Action.AUTH
    assert action.payload == {"id": 10}


@test("sign action")
async def _():
    action = PastaportoAction(action=Action.AUTH, payload={"test": "payload"})

    with time_machine.travel("2020-10-10 10:10:10", tick=False):
        token = action.sign("test")
        decoded_token = jwt.decode(token, "test", algorithms=["HS256"])

        assert decoded_token["action"] == "auth"
        assert decoded_token["payload"] == {"test": "payload"}
        assert decoded_token["exp"] == timegm(
            (datetime.utcnow() + timedelta(seconds=40)).utctimetuple()
        )
        assert decoded_token["iat"] == timegm(datetime.utcnow().utctimetuple())
