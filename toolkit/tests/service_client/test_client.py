from dataclasses import dataclass
from typing import Any, Dict, List
from unittest.mock import patch

from pythonit_toolkit.api.service_client import ServiceClient
from ward import test


@dataclass
class MockResponse:
    data: List[Dict[str, Any]]

    async def json(self):
        print("take your data!")
        return self.data


@test("get a user")
async def _():
    query = """
        query{
            users {
                id
            }
        }
    """
    mock_data = [
        {
            "id": 1,
        },
    ]

    with patch("httpx.AsyncClient.post") as post_mock:
        post_mock.return_value = MockResponse(mock_data)
        cleint = ServiceClient(
            jwt_secret="mysecret",
        )

        response = await cleint.execute(
            document=query, issuer="pycon", audience="users-service"
        )

        assert response == mock_data
