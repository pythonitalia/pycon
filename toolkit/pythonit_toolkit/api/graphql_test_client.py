import json
import logging
from collections import namedtuple
from dataclasses import dataclass
from typing import Any, Dict, Optional

from pythonit_toolkit.headers import PASTAPORTO_X_HEADER, SERVICE_JWT_HEADER
from pythonit_toolkit.pastaporto.test import (
    fake_pastaporto_token_for_user,
    fake_service_to_service_token,
)

logger = logging.getLogger(__name__)


SimulatedUser = namedtuple("User", ["id", "email", "is_staff"])


@dataclass
class Response:
    errors: Optional[Dict[str, Any]]
    data: Optional[Dict[str, Any]]


class GraphQLClient:
    def __init__(
        self,
        client,
        *,
        pastaporto_secret: Optional[str] = None,
        service_to_service_secret: Optional[str] = None,
        admin_endpoint: bool = False,
        internal_api_endpoint: bool = False
    ):
        self._client = client
        self._pastaporto_secret = pastaporto_secret
        self._service_to_service_secret = service_to_service_secret
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

    def force_login(self, user: SimulatedUser):
        self.pastaporto_token = fake_pastaporto_token_for_user(
            {"id": user.id, "email": user.email},
            str(self._pastaporto_secret),
            staff=user.is_staff,
        )

    def force_service_login(self, key: Optional[str] = None):
        self.service_to_service_token = fake_service_to_service_token(
            str(key or self._service_to_service_secret),
            issuer="gateway",
            audience="users-service",
        )
