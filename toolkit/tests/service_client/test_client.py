from unittest.mock import AsyncMock, patch

from pythonit_toolkit.service_client import ServiceClient
from ward import raises, test


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
            caller="pycon",
            service_name="users-service",
            jwt_secret="mysecret",
        )

        response = await client.execute(document=query)

        assert response.data == {"users": [{"id": 1}]}


@test("return errors when an exception is thrown in the service")
async def _():

    mock_response = {"errors": [{"message": "something went wrong"}]}

    with raises(Exception) as exc, patch("httpx.AsyncClient.post") as post_mock:
        post_mock.return_value = AsyncMock()
        post_mock.return_value.json.return_value = mock_response

        client = ServiceClient(
            url="http://localhost:8050",
            caller="pycon",
            service_name="users-service",
            jwt_secret="mysecret",
        )

        await client.execute(document="""{ users { id }}""")

    assert exc.raised.errors == [{"message": "something went wrong"}]


@test("url is required when creating the ServiceClient instance")
def _():
    with raises(ValueError) as exc:
        ServiceClient(
            url="",
            caller="pycon",
            service_name="users-service",
            jwt_secret="mysecret",
        )

    assert str(exc.raised) == "Argument 'url' can't be empty"


@test("caller is required when creating the ServiceClient instance")
def _():
    with raises(ValueError) as exc:
        ServiceClient(
            url="http://localhost:8050",
            caller="",
            service_name="users-service",
            jwt_secret="mysecret",
        )

    assert str(exc.raised) == "Argument 'caller' can't be empty"


@test("service_name is required when creating the ServiceClient instance")
def _():
    with raises(ValueError) as exc:
        ServiceClient(
            url="http://localhost:8050",
            caller="pycon",
            service_name="",
            jwt_secret="mysecret",
        )

    assert str(exc.raised) == "Argument 'service_name' can't be empty"


@test("jwt_secret is required when creating the ServiceClient instance")
def _():
    with raises(ValueError) as exc:
        ServiceClient(
            url="http://localhost:8050",
            caller="pycon",
            service_name="users-service",
            jwt_secret="",
        )

    assert str(exc.raised) == "Argument 'jwt_secret' can't be empty"
