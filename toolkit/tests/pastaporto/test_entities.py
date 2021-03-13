import time_machine
from pythonit_toolkit.pastaporto.entities import Credential, Pastaporto
from pythonit_toolkit.pastaporto.exceptions import InvalidPastaportoError
from pythonit_toolkit.pastaporto.test import fake_pastaporto_token_for_user
from ward import raises, test


@test("create pastaporto object from token")
def _():
    token = fake_pastaporto_token_for_user(
        {"id": 1, "email": "test@email.it"}, "secret", staff=False
    )
    pastaporto = Pastaporto.from_token(token, "secret")

    assert pastaporto.user_info.id == 1
    assert pastaporto.user_info.email == "test@email.it"
    assert pastaporto.credentials == [Credential.AUTHENTICATED]


@test("create pastaporto for staff user")
def _():
    token = fake_pastaporto_token_for_user(
        {"id": 1, "email": "test@email.it"}, "secret", staff=True
    )
    pastaporto = Pastaporto.from_token(token, "secret")

    assert pastaporto.user_info.id == 1
    assert pastaporto.user_info.email == "test@email.it"
    assert pastaporto.credentials == [Credential.AUTHENTICATED, Credential.STAFF]


@test("cannot create pastaporto from expired tokens")
def _():
    with time_machine.travel("2010-10-10 10:10:10"):
        token = fake_pastaporto_token_for_user(
            {"id": 1, "email": "test@email.it"}, "secret", staff=True
        )

    with time_machine.travel("2021-10-10 10:10:10"), raises(InvalidPastaportoError):
        Pastaporto.from_token(token, "secret")


@test("cannot create pastaporto with wrong secret")
def _():
    with time_machine.travel("2010-10-10 10:10:10"):
        token = fake_pastaporto_token_for_user(
            {"id": 1, "email": "test@email.it"}, "secret", staff=True
        )

    with time_machine.travel("2021-10-10 10:10:10"), raises(InvalidPastaportoError):
        Pastaporto.from_token(token, "another")
