from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from unittest.mock import patch

from pythonit_toolkit.api.client import Client
from ward import test


@dataclass
class MockResponse:
    data: Optional[List[Dict[str, Any]]]
    status_code: int

    def json(self):
        return self.data


class MockResponseAsync:
    def __init__(self, json_data, status_code):
        self.response = MockResponse(data=json_data, status_code=status_code)

    async def getResponse(self):
        return self.response


@test("get a user")
async def _():

    with patch("httpx.AsyncClient") as mock_post:
        async_response = MockResponseAsync([], 200)
        mock_post.return_value.post.return_value = await async_response.getResponse()

        response = await Client().user(1)
        print(response)
        assert response == []
