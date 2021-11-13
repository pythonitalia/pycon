from dataclasses import dataclass
from typing import Any, Optional, Union

import httpx
from pythonit_toolkit.headers import SERVICE_JWT_HEADER
from pythonit_toolkit.pastaporto.tokens import generate_service_to_service_token


@dataclass
class ServiceResponse:
    data: Optional[dict[str, Any]]


@dataclass
class ServiceError(Exception):
    errors: list[dict[str, Any]]


class ServiceClient:
    def __init__(
        self,
        url: str,
        caller: str,
        service_name: str,
        jwt_secret: str,
    ):
        self.url = url
        self.caller = caller
        self.service_name = service_name
        self.jwt_secret = jwt_secret

        for arg in ("url", "caller", "service_name", "jwt_secret"):
            if not getattr(self, arg):
                raise ValueError(f"Argument '{arg}' can't be empty")

    async def execute(
        self,
        document: str,
        variables: Optional[dict[str, Any]] = None,
    ) -> Union[ServiceError, ServiceResponse]:
        token = generate_service_to_service_token(
            self.jwt_secret, issuer=self.caller, audience=self.service_name
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
            errors = data.get("errors", None)

            if errors:
                raise ServiceError(errors)

            return ServiceResponse(data=data.get("data"))
