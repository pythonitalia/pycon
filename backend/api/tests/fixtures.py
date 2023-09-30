import dataclasses
import json
from typing import Any, Dict, Optional

import pytest
import respx
from django.conf import settings
from django.test import Client as DjangoTestClient


def query_wrapper(original):
    def call(*args, **kwargs):
        response = original(*args, **kwargs)
        response_dict = dataclasses.asdict(response)

        if response_dict.get("errors") is None:
            response_dict.pop("errors")

        return response_dict

    return call


# GraphQLClient.query = query_wrapper(async_to_sync(GraphQLClient.query))


class DjangoAsyncClientWrapper:
    def __init__(self, client) -> None:
        self.client = client

    async def post(self, *args, **kwargs):
        headers = kwargs.pop("headers", {})
        data = json.dumps(kwargs.pop("json"))
        content_type = "application/json"
        return await self.client.post(
            *args, data=data, content_type=content_type, **kwargs, **headers
        )


class NewGraphQLClient:
    def __init__(self):
        self.client = DjangoTestClient()

    def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        body = {"query": query}
        headers = headers or {}

        if variables:
            body["variables"] = variables

        resp = self.client.post(
            "/graphql", data=body, headers=headers, content_type="application/json"
        )
        data = json.loads(resp.content.decode())
        # return GraphQLResponse(errors=data.get("errors"), data=data.get("data"))
        return data

    def force_login(self, user):
        self.client.force_login(user)


@pytest.fixture()
def graphql_client(async_client):
    return NewGraphQLClient()
    # return GraphQLClient(
    #     DjangoAsyncClientWrapper(async_client),
    #     pastaporto_secret=settings.PASTAPORTO_SECRET,
    # )


@pytest.fixture()
def admin_graphql_client(async_client):
    raise ValueError("fix me")
    # graphql_client = GraphQLClient(
    #     DjangoAsyncClientWrapper(async_client),
    #     pastaporto_secret=settings.PASTAPORTO_SECRET,
    # )
    # graphql_client.force_login(
    # SimulatedUser(id=1, email="test@user.it", is_staff=True)
    # )
    # return graphql_client


@pytest.fixture
def mock_users_by_ids(mocker):
    with respx.mock as mock:
        mock.post(f"{settings.USERS_SERVICE_URL}/internal-api").respond(
            json={
                "data": {
                    "usersByIds": [
                        {
                            "id": 10,
                            "fullname": "Marco Acierno",
                            "name": "Marco",
                            "username": "marco",
                            "gender": "male",
                            "email": "marco@placeholder.it",
                        }
                    ]
                }
            }
        )

        yield
