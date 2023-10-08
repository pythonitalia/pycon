import dataclasses
import json
from typing import Any, Dict, Optional

import pytest
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
    def __init__(self, *, include_full_response: bool = False):
        self.client = DjangoTestClient()
        self.include_full_response = include_full_response

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

        if self.include_full_response:
            return data, resp
        return data

    def force_login(self, user):
        self.client.force_login(user)


@pytest.fixture()
def graphql_client():
    return NewGraphQLClient()


@pytest.fixture()
def full_response_graphql_client():
    return NewGraphQLClient(include_full_response=True)


@pytest.fixture()
def admin_graphql_client(graphql_client):
    from users.tests.factories import UserFactory

    admin_user = UserFactory(is_staff=True, is_superuser=True)
    graphql_client.force_login(admin_user)
    return graphql_client
