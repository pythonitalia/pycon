import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

from pythonit_toolkit.pastaporto.test import (
    fake_pastaporto_token_for_user,
    fake_service_to_service_token,
)
from pythonit_toolkit.starlette_backend.pastaporto_backend import PASTAPORTO_X_HEADER
from ward import fixture

from users.domain import entities
from users.settings import (
    PASTAPORTO_SECRET,
    SERVICE_JWT_HEADER,
    SERVICE_TO_SERVICE_SECRET,
)
from users.tests.client import testclient

logger = logging.getLogger(__name__)


@dataclass
class Response:
    errors: Optional[Dict[str, Any]]
    data: Optional[Dict[str, Any]]


class GraphQLClient:
    def __init__(
        self, client, admin_endpoint: bool = False, internal_api_endpoint: bool = False
    ):
        self._client = client
        self.pastaporto_token = None
        self.service_to_service_token = None

        if internal_api_endpoint:
            self.endpoint = "/internal-api"
        elif admin_endpoint:
            self.endpoint = "/admin-api"
        else:
            self.endpoint = "/graphql"

    async def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> Response:
        body = {"query": query}
        headers = headers or {}

        if variables:
            body["variables"] = variables

        if self.pastaporto_token:
            headers[PASTAPORTO_X_HEADER] = self.pastaporto_token

        if self.service_to_service_token:
            headers[SERVICE_JWT_HEADER] = self.service_to_service_token

        resp = await self._client.post(self.endpoint, json=body, headers=headers)
        data = json.loads(resp.content.decode())
        return Response(errors=data.get("errors"), data=data.get("data"))

    def force_login(self, user: entities.User):
        self.pastaporto_token = fake_pastaporto_token_for_user(
            {"id": user.id, "email": user.email},
            str(PASTAPORTO_SECRET),
            staff=user.is_staff,
        )

    def force_service_login(self, key: str = SERVICE_TO_SERVICE_SECRET):
        self.service_to_service_token = fake_service_to_service_token(
            str(key), issuer="gateway", audience="users-service"
        )


@fixture()
async def graphql_client(testclient=testclient):
    async with testclient:
        yield GraphQLClient(testclient)


@fixture()
async def admin_graphql_client(testclient=testclient):
    async with testclient:
        yield GraphQLClient(testclient, admin_endpoint=True)


@fixture()
async def internalapi_graphql_client(testclient=testclient):
    async with testclient:
        yield GraphQLClient(testclient, internal_api_endpoint=True)
