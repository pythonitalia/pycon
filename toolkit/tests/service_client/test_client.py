from dataclasses import dataclass
from typing import Any, Optional
from unittest.mock import patch

from pythonit_toolkit.api.service_client import ServiceClient
from ward import test


@dataclass
class MockResponse:
    return_value: Optional[Any] = None

    async def json(self):
        return self.return_value


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

    with patch("httpx.AsyncClient.post") as post_mock:
        post_mock.return_value = MockResponse(return_value=mock_response)
        cleint = ServiceClient(
            url="http://localhost:8050",
            issuer="pycon",
            audience="users-service",
            jwt_secret="mysecret",
        )

        response = await cleint.execute(document=query)

        assert response.data == {"users": [{"id": 1}]}
