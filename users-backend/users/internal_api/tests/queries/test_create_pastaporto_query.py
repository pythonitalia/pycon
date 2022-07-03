import jwt
import time_machine
from pythonit_toolkit.pastaporto.entities import Credential
from pythonit_toolkit.pastaporto.tokens import decode_pastaporto
from ward import each, test

from users.settings import PASTAPORTO_SECRET
from users.tests.api import internalapi_graphql_client
from users.tests.factories import user_factory
from users.tests.session import db


@test("create pastaporto for user")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login()
    user = await user_factory(email="testuser@user.it", is_staff=False)

    query = """query($token: String) {
        createPastaporto(identityToken: $token) {
            pastaportoToken
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"token": user.create_identity_token()}
    )

    assert not response.errors
    token = response.data["createPastaporto"]["pastaportoToken"]
    pastaporto = decode_pastaporto(token, PASTAPORTO_SECRET)

    assert pastaporto["user_info"]["id"] == user.id
    assert pastaporto["user_info"]["email"] == user.email
    assert pastaporto["user_info"]["is_staff"] == user.is_staff
    assert pastaporto["credentials"] == [Credential.AUTHENTICATED]


@test("create pastaporto for invalid token {token_to_try} is not authenticated")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
    token_to_try=each("", None),
):
    internalapi_graphql_client.force_service_login()

    query = """query($token: String) {
        createPastaporto(identityToken: $token) {
            pastaportoToken
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"token": token_to_try}
    )

    assert not response.errors
    token = response.data["createPastaporto"]["pastaportoToken"]
    pastaporto = decode_pastaporto(token, PASTAPORTO_SECRET)

    assert pastaporto["user_info"] is None
    assert pastaporto["credentials"] == []


@test("not active user doesn't create token")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login()
    user = await user_factory(email="testuser@user.it", is_staff=False, is_active=False)

    query = """query($token: String) {
        createPastaporto(identityToken: $token) {
            pastaportoToken
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"token": user.create_identity_token()}
    )

    assert not response.errors
    token = response.data["createPastaporto"]["pastaportoToken"]
    pastaporto = decode_pastaporto(token, PASTAPORTO_SECRET)

    assert pastaporto["user_info"] is None
    assert pastaporto["credentials"] == []


@test("invalid identity token is rejected")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login()
    await user_factory(email="testuser@user.it", is_staff=False, is_active=False)

    query = """query($token: String) {
        createPastaporto(identityToken: $token) {
            pastaportoToken
        }
    }"""

    response = await internalapi_graphql_client.query(
        query, variables={"token": "random_value"}
    )

    assert response.errors[0]["message"] == "Identity token is not valid"
    assert not response.data


@test("expired identity is rejected")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login()
    user = await user_factory(email="testuser@user.it", is_staff=False, is_active=False)

    with time_machine.travel("2020-10-10 10:00:00", tick=False):
        expired_token = user.create_identity_token()

    query = """query($token: String) {
        createPastaporto(identityToken: $token) {
            pastaportoToken
        }
    }"""

    with time_machine.travel("2022-03-03 10:00:00", tick=False):
        response = await internalapi_graphql_client.query(
            query, variables={"token": expired_token}
        )

    assert response.errors[0]["message"] == "Identity token is not valid"
    assert not response.data


@test("identity signed with a different key is rejected")
async def _(
    internalapi_graphql_client=internalapi_graphql_client,
    db=db,
    user_factory=user_factory,
):
    internalapi_graphql_client.force_service_login()
    await user_factory(email="testuser@user.it", is_staff=False, is_active=False)

    invalid_token = jwt.encode({}, "invalidme")

    query = """query($token: String) {
        createPastaporto(identityToken: $token) {
            pastaportoToken
        }
    }"""

    with time_machine.travel("2022-03-03 10:00:00", tick=False):
        response = await internalapi_graphql_client.query(
            query, variables={"token": invalid_token}
        )

    assert response.errors[0]["message"] == "Identity token is not valid"
    assert not response.data
