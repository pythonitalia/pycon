import os
from typing import Any, Dict, Optional

import httpx
import jwt
from pythonit_toolkit.headers import SERVICE_JWT_HEADER

INTERNAL_JWT_SECRET = os.getenv("INTERNAL_JWT_SECRET", "a-very-secret-secret")


class Client:
    url = "/internal-api"

    async def execute(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
    ):
        token = jwt.encode({"some": "payload"}, INTERNAL_JWT_SECRET, algorithm="HS256")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                data={"query": query, "variables": variables},
                headers={
                    SERVICE_JWT_HEADER: token,
                },
            )

            data = await response.json()
            return data

    def users(self):
        query = """
            query{
                 users {
                    id
                    fullname
                    name
                    email
                    gender
                    dateBirth
                    openToRecruiting
                    openToNewsletter
                    country
                    isActive
                    isStaff
                }
            }
        """

        return self.execute(
            query,
        )
