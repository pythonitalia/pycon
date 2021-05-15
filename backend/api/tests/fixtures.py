import dataclasses
import json

import pytest
from asgiref.sync import async_to_sync
from django.conf import settings
from pythonit_toolkit.api.graphql_test_client import GraphQLClient, SimulatedUser


def query_wrapper(original):
    def call(*args, **kwargs):
        response = original(*args, **kwargs)
        response_dict = dataclasses.asdict(response)

        if response_dict.get("errors") is None:
            response_dict.pop("errors")

        return response_dict

    return call


GraphQLClient.query = query_wrapper(async_to_sync(GraphQLClient.query))


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


@pytest.fixture()
def graphql_client(async_client):
    return GraphQLClient(
        DjangoAsyncClientWrapper(async_client),
        pastaporto_secret=settings.PASTAPORTO_SECRET,
    )


@pytest.fixture()
def admin_graphql_client(async_client):
    graphql_client = GraphQLClient(
        DjangoAsyncClientWrapper(async_client),
        pastaporto_secret=settings.PASTAPORTO_SECRET,
    )
    graphql_client.force_login(SimulatedUser(id=1, email="test@user.it", is_staff=True))
    return graphql_client
