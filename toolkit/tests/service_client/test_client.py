import json

import respx
from pythonit_toolkit.headers import SERVICE_JWT_HEADER
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

    with respx.mock as req_mock:
        url_mock = req_mock.post("http://localhost:8050/internal-api").respond(
            200, json=mock_response
        )

        client = ServiceClient(
            url="http://localhost:8050/internal-api",
            caller="pycon",
            service_name="users-backend",
            jwt_secret="mysecret",
        )

        response = await client.execute(document=query)

        assert url_mock.called
        call = url_mock.calls[0]

        # Make sure we send the JWT header
        assert SERVICE_JWT_HEADER in call.request.headers

        # Make sure the GraphQL request looks ok
        content_sent = json.loads(call.request.content)
        assert "users {" in content_sent["query"]
        assert content_sent["variables"] is None
        assert response.data == {"users": [{"id": 1}]}


@test("return errors when an exception is thrown in the service")
async def _():
    mock_response = {"errors": [{"message": "something went wrong"}]}

    with raises(Exception) as exc, respx.mock as req_mock:
        req_mock.post("http://localhost:8050/internal-api").respond(
            200, json=mock_response
        )

        client = ServiceClient(
            url="http://localhost:8050/internal-api",
            caller="pycon",
            service_name="users-backend",
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
            service_name="users-backend",
            jwt_secret="mysecret",
        )

    assert str(exc.raised) == "Argument 'url' can't be empty"


@test("caller is required when creating the ServiceClient instance")
def _():
    with raises(ValueError) as exc:
        ServiceClient(
            url="http://localhost:8050",
            caller="",
            service_name="users-backend",
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
            service_name="users-backend",
            jwt_secret="",
        )

    assert str(exc.raised) == "Argument 'jwt_secret' can't be empty"
