import time_machine
from sqlalchemy.sql.expression import select
from ward import test

from users.domain.entities import User
from users.domain.repository import UsersRepository
from users.tests.factories import user_factory
from users.tests.graphql_client import graphql_client
from users.tests.session import db


@test("reset password")
async def _(graphql_client=graphql_client, db=db, user_factory=user_factory):
    user = await user_factory(email="test@email.it", password="hello", jwt_auth_id=1)

    query = """
    mutation($input: ResetPasswordInput!) {
        resetPassword(input: $input) {
            __typename
        }
    }
    """
    response = await graphql_client.query(
        query,
        variables={
            "input": {
                "token": user.create_reset_password_token(),
                "newPassword": "newpassword",
            }
        },
    )

    assert not response.errors
    assert response.data["resetPassword"]["__typename"] == "OperationSuccess"

    query = select(User).where(User.email == "test@email.it")
    raw_query_user: User = (await db.execute(query)).scalar()
    assert raw_query_user.check_password("newpassword")
    assert raw_query_user.jwt_auth_id == 2


@test("cannot reset password with short password")
async def _(graphql_client=graphql_client, db=db, user_factory=user_factory):
    user = await user_factory(email="test@email.it", password="hello", jwt_auth_id=1)

    query = """
    mutation($input: ResetPasswordInput!) {
        resetPassword(input: $input) {
            __typename

            ... on ResetPasswordValidationError {
                errors {
                    newPassword {
                        type
                        message
                    }
                }
            }
        }
    }
    """
    response = await graphql_client.query(
        query,
        variables={
            "input": {"token": user.create_reset_password_token(), "newPassword": "new"}
        },
    )

    assert not response.errors
    assert (
        response.data["resetPassword"]["__typename"] == "ResetPasswordValidationError"
    )
    assert response.data["resetPassword"]["errors"]["newPassword"] == [
        {
            "type": "value_error.any_str.min_length",
            "message": "ensure this value has at least 8 characters",
        }
    ]

    query = select(User).where(User.email == "test@email.it")
    raw_query_user: User = (await db.execute(query)).scalar()
    assert raw_query_user.check_password("hello")
    assert raw_query_user.jwt_auth_id == 1


@test("cannot reset password with expired token")
async def _(graphql_client=graphql_client, db=db, user_factory=user_factory):
    user = await user_factory(email="test@email.it", password="hello")

    with time_machine.travel("2020-10-10 15:00:00", tick=False):
        token = user.create_reset_password_token()

    query = """
    mutation($input: ResetPasswordInput!) {
        resetPassword(input: $input) {
            __typename

            ... on ResetPasswordTokenExpired {
                message
            }
        }
    }
    """

    with time_machine.travel("2020-10-13 15:00:00", tick=False):
        response = await graphql_client.query(
            query,
            variables={"input": {"token": token, "newPassword": "newpasswordtest"}},
        )

    assert not response.errors
    assert response.data["resetPassword"]["__typename"] == "ResetPasswordTokenExpired"
    query = select(User).where(User.email == "test@email.it")
    raw_query_user: User = (await db.execute(query)).scalar()
    assert raw_query_user.check_password("hello")


@test("cannot reset password of not active user")
async def _(graphql_client=graphql_client, db=db, user_factory=user_factory):
    user = await user_factory(email="test@email.it", password="hello", is_active=False)

    token = user.create_reset_password_token()

    query = """
    mutation($input: ResetPasswordInput!) {
        resetPassword(input: $input) {
            __typename

            ... on ResetPasswordTokenInvalid {
                message
            }
        }
    }
    """

    response = await graphql_client.query(
        query, variables={"input": {"token": token, "newPassword": "newpasswordtest"}}
    )

    assert not response.errors
    assert response.data["resetPassword"]["__typename"] == "ResetPasswordTokenInvalid"
    query = select(User).where(User.email == "test@email.it")
    raw_query_user: User = (await db.execute(query)).scalar()
    assert raw_query_user.check_password("hello")


@test("cannot reset password with token invalidated by new id")
async def _(graphql_client=graphql_client, db=db, user_factory=user_factory):
    user = await user_factory(
        email="test@email.it",
        password="hello",
        is_active=True,
        jwt_auth_id=1,
    )

    token = user.create_reset_password_token()

    db_query = select(User).where(User.id == user.id)
    raw_query_user: User = (await db.execute(db_query)).scalar()
    raw_query_user.jwt_auth_id = 2
    repository = UsersRepository(db)
    await repository.save_user(raw_query_user)
    await repository.commit()

    query = """
    mutation($input: ResetPasswordInput!) {
        resetPassword(input: $input) {
            __typename

            ... on ResetPasswordTokenInvalid {
                message
            }
        }
    }
    """

    response = await graphql_client.query(
        query, variables={"input": {"token": token, "newPassword": "newpasswordtest"}}
    )

    assert not response.errors
    assert response.data["resetPassword"]["__typename"] == "ResetPasswordTokenInvalid"

    query = select(User).where(User.email == "test@email.it")
    raw_query_user: User = (await db.execute(query)).scalar()
    assert raw_query_user.check_password("hello")
