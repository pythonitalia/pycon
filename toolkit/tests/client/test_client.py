from dataclasses import dataclass
from typing import Any, Dict, List
from unittest.mock import patch

from pythonit_toolkit.api.client import Client
from ward import test


@dataclass
class MockResponse:
    data: List[Dict[str, Any]]

    async def json(self):
        print("take your data!")
        return self.data


@test("get a user")
async def _():
    with patch("httpx.AsyncClient.post") as post_mock:
        post_mock.return_value = MockResponse([{"id": 1}])

        response = await Client().user(1)

        assert response == [{"id": 1}]
