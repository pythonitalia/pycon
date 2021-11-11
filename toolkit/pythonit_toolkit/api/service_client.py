from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx
from pythonit_toolkit.headers import SERVICE_JWT_HEADER
from pythonit_toolkit.pastaporto.tokens import generate_service_to_service_token


@dataclass
class ServiceResponse:
    errors: Optional[Dict[str, Any]]
    data: Optional[Dict[str, Any]]


class ServiceClient:
    def __init__(
        self,
        url: str,
        issuer: str,
        audience: str,
        jwt_secret: str,
    ):
        self.url = url
        self.issuer = issuer
        self.audience = audience
        self.jwt_secret = jwt_secret

        for arg in ("url", "issuer", "audience", "jwt_secret"):
            if not getattr(self, arg):
                raise ValueError(f"Argument '{arg}' can't be empty")

    async def execute(
        self,
        document: str,
        variables: Optional[Dict[str, Any]] = None,
    ):
        token = generate_service_to_service_token(
            self.jwt_secret, issuer=self.issuer, audience=self.audience
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                data={"query": document, "variables": variables},
                headers={
                    SERVICE_JWT_HEADER: token,
                },
            )

            response.raise_for_status()

            data = await response.json()
            return ServiceResponse(errors=data.get("errors"), data=data.get("data"))
