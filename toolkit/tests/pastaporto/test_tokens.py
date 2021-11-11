from datetime import datetime, timedelta, timezone

import jwt
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
    token = generate_service_to_service_token("secret", issuer="me", audience="you")

    assert (
        token
        == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3N1ZXIiOiJtZSIsImF1ZGllbmNlIjoieW91IiwiZXhwaXJlc19pbiI6IjFtIn0.ZXNfbPE8osJRQU4ZCH3CWSm0bZyUukBzy6rkResdTYQ"
    )


@test("raise ValueError if secret is empty")
async def _():

    with raises(ValueError) as exc:
        generate_service_to_service_token("", issuer="me", audience="you")

    assert str(exc.raised) == "Secret can not be empty"
