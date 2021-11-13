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


@test("Generate a service to service token")
async def _():
    with time_machine.travel("2021-11-13 18:41:10", tick=False):

        token = generate_service_to_service_token("secret", issuer="me", audience="you")

        assert (
            token
            == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJtZSIsImF1ZCI6InlvdSIsImlhdCI6MTYzNjgyODg3MCwiZXhwIjoxNjM2ODI4OTMwfQ.LnS-GDGazo6q5-54h9oGCmixRwA84QJX7I-TnU3gEvI"
        )


@test("Secret is required when creating a service-to-service token")
async def _():

    with raises(ValueError) as exc:
        generate_service_to_service_token("", issuer="me", audience="you")

    assert str(exc.raised) == "Secret can not be empty"
