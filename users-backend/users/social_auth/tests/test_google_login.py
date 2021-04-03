from typing import cast
from unittest.mock import patch

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select
from ward import test

from users.domain.entities import User
from users.tests.client import testclient
from users.tests.factories import user_factory
from users.tests.session import db


@test("social login creates a new account if it does not exist")
async def _(testclient=testclient, db=db):
    db = cast(AsyncSession, db)

    query = select(User).where(User.email == "google@user.it")
    db_user: User = (await db.execute(query)).scalar()

    assert not db_user

    with patch("users.social_auth.views.oauth.google.authorize_access_token"), patch(
        "users.social_auth.views.oauth.google.parse_id_token"
    ) as parse_id_mock:
        parse_id_mock.return_value = {
            "email": "google@user.it",
            "sub": "10001001010",
            "name": "Nina Nana",
            "email_verified": True,
            "given_name": "Nina",
            "family_name": "Nana",
        }

        response = await testclient.get("/login/google/auth")

    assert response.status_code == 200
    query = select(User).where(User.email == "google@user.it")
    db_user: User = (await db.execute(query)).scalar()

    assert db_user
    assert db_user.fullname == "Nina Nana"
    assert db_user.name == "Nina"
    assert not db_user.has_usable_password()


@test("social login to account with same email")
async def _(
    testclient=testclient,
    user_factory=user_factory,
    db=db,
):
    db = cast(AsyncSession, db)

    existent_user = await user_factory(
        email="i@exist.it", fullname="I Already", name="Exist"
    )
    await db.commit()

    with patch("users.social_auth.views.oauth.google.authorize_access_token"), patch(
        "users.social_auth.views.oauth.google.parse_id_token"
    ) as parse_id_mock:
        parse_id_mock.return_value = {
            "email": "i@exist.it",
            "sub": "10001001010",
            "name": "Nina Nana",
            "email_verified": True,
            "given_name": "Nina",
            "family_name": "Nana",
        }

        response = await testclient.get("/login/google/auth")

    assert response.status_code == 200

    query = select(User).where(User.email == existent_user.email)
    db_user: User = (await db.execute(query)).scalar()

    assert db_user
    assert db_user.fullname == "I Already"
    assert db_user.name == "Exist"


@test("reject google account if the email is not verified")
async def _(testclient=testclient, db=db):
    db = cast(AsyncSession, db)

    with patch("users.social_auth.views.oauth.google.authorize_access_token"), patch(
        "users.social_auth.views.oauth.google.parse_id_token"
    ) as parse_id_mock:
        parse_id_mock.return_value = {
            "email": "i@exist.it",
            "sub": "10001001010",
            "name": "Nina Nana",
            "email_verified": False,
            "given_name": "Nina",
            "family_name": "Nana",
        }

        response = await testclient.get("/login/google/auth")

    assert response.status_code == 400
    query = select(User).where(User.email == "i@exist.it")
    db_user: User = (await db.execute(query)).scalar()

    assert not db_user
