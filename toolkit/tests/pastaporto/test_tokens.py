from datetime import datetime, timedelta, timezone

import jwt
import time_machine
from pythonit_toolkit.pastaporto.tokens import (
    decode_service_to_service_token,
    generate_service_to_service_token,
)
from ward import raises, test


@test("decode service to service")
async def _():
    test_token = jwt.encode(
        {
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(seconds=10),
            "iss": "test",
            "aud": "users-service",
        },
        "secret",
        algorithm="HS256",
    )

    decode_service_to_service_token(
        test_token, "secret", issuer="test", audience="users-service"
    )


@test("reject tokens without expiration")
async def _():
    test_token = jwt.encode(
        {"iat": datetime.now(timezone.utc), "iss": "test", "aud": "users-service"},
        "secret",
        algorithm="HS256",
    )

    with raises(jwt.MissingRequiredClaimError):
        decode_service_to_service_token(
            test_token, "secret", issuer="test", audience="users-service"
        )


@test("reject tokens without audience")
async def _():
    test_token = jwt.encode(
        {
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(seconds=10),
            "iss": "test",
        },
        "secret",
        algorithm="HS256",
    )

    with raises(jwt.MissingRequiredClaimError):
        decode_service_to_service_token(
            test_token, "secret", issuer="test", audience="users-service"
        )


@test("reject tokens with different audience")
async def _():
    test_token = jwt.encode(
        {
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(seconds=10),
            "iss": "test",
            "aud": "users-service",
        },
        "secret",
        algorithm="HS256",
    )

    with raises(jwt.InvalidAudienceError):
        decode_service_to_service_token(
            test_token, "secret", issuer="test", audience="association-backend"
        )


@test("generate a token")
async def _():
    with time_machine.travel("2021-11-13 18:41:10", tick=False):

        token = generate_service_to_service_token("secret", issuer="me", audience="you")

        assert (
            token
            == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJtZSIsImF1ZCI6InlvdSIsImV4cCI6MTYzNjgyODkzMH0.USy6g043fdWG35yCIM021GXQHUp7L0HO8PHUPKRDAD4"
        )


@test("raise ValueError if secret is empty")
async def _():

    with raises(ValueError) as exc:
        generate_service_to_service_token("", issuer="me", audience="you")

    assert str(exc.raised) == "Secret can not be empty"
