from dataclasses import dataclass
from typing import Any, Optional, Type
from unittest.mock import patch

from pythonit_toolkit.api.service_client import ServiceClient
from ward import raises, test


@dataclass
class MockResponse:
    return_value: Optional[Any] = None
    side_effect: Optional[Type] = None

    async def json(self):
        return self.return_value

    def raise_for_status(self):
        if self.side_effect:
            raise self.side_effect
        return True


@test("execute a query")
async def _():
    query = """
        query{
            users {
                id
            }
        }
    """
    mock_response = {"data": {"users": [{"id": 1}]}}

    with patch("httpx.AsyncClient.post") as post_mock:
        post_mock.return_value = MockResponse(return_value=mock_response)
        client = ServiceClient(
            url="http://localhost:8050",
            issuer="pycon",
            audience="users-service",
            jwt_secret="mysecret",
        )

        response = await client.execute(document=query)

        assert response.data == {"users": [{"id": 1}]}


@test("raise Exception")
async def _():

    with raises(Exception), patch("httpx.AsyncClient.post") as post_mock:
        post_mock.return_value = MockResponse(
            side_effect=Exception("Something went wrong")
        )

        client = ServiceClient(
            url="http://localhost:8050",
            issuer="pycon",
            audience="users-service",
            jwt_secret="mysecret",
        )

        await client.execute(document="""{ users { id }}""")


for url, issuer, audience, jwt_secret, expected_error in [
    ("", "pycon", "users-service", "mysecret", "Argument 'url' can't be empty"),
    (
        "http://localhost:8050",
        "",
        "users-service",
        "mysecret",
        "Argument 'issuer' can't be empty",
    ),
    (
        "http://localhost:8050",
        "pycon",
        "",
        "mysecret",
        "Argument 'audience' can't be empty",
    ),
    (
        "http://localhost:8050",
        "pycon",
        "users-service",
        "",
        "Argument 'jwt_secret' can't be empty",
    ),
]:

    @test("raise ValueError if arguments are empty")
    async def _():

        with raises(ValueError) as exc:
            ServiceClient(
                url=url,
                issuer=issuer,
                audience=audience,
                jwt_secret=jwt_secret,
            )

        assert str(exc.raised) == expected_error
