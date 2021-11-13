from unittest.mock import AsyncMock, patch

from pythonit_toolkit.api.service_client import ServiceClient
from ward import each, raises, test


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
        post_mock.return_value = AsyncMock()
        post_mock.return_value.json.return_value = mock_response

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
        post_mock.return_value = AsyncMock()
        post_mock.return_value.json.side_effect = Exception("Something went wrong")

        client = ServiceClient(
            url="http://localhost:8050",
            issuer="pycon",
            audience="users-service",
            jwt_secret="mysecret",
        )

        response = await client.execute(document="""{ users { id }}""")

        assert response.errors == ["Something went wrong"]


@test("raise ValueError if arguments are empty")
async def _(
    url=each(
        "",
        "http://localhost:8050",
        "http://localhost:8050",
        "http://localhost:8050",
    ),
    issuer=each(
        "pycon",
        "",
        "pycon",
        "pycon",
    ),
    audience=each(
        "users-service",
        "users-service",
        "",
        "users-service",
    ),
    jwt_secret=each(
        "mysecret",
        "mysecret",
        "mysecret",
        "",
    ),
    missing_argument=each(
        "url",
        "issuer",
        "audience",
        "jwt_secret",
    ),
):

    with raises(ValueError) as exc:
        ServiceClient(
            url=url,
            issuer=issuer,
            audience=audience,
            jwt_secret=jwt_secret,
        )

    assert str(exc.raised) == f"Argument '{missing_argument}' can't be empty"
