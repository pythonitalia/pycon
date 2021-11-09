from typing import Any, Dict, Optional

import httpx
from pythonit_toolkit.headers import SERVICE_JWT_HEADER
from pythonit_toolkit.pastaporto.tokens import generate_token


class ServiceClient:
    url = "/internal-api"

    def __init__(self, jwt_secret: str, issuer: str, audience: str):
        self.jwt_secret = jwt_secret
        self.issuer = issuer
        self.audience = audience

    async def execute(
        self,
        document: str,
        variables: Optional[Dict[str, Any]] = None,
    ):
        token = generate_token(
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

            data = await response.json()
            return data
