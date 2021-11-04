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
    mock_data = [
        {
            "id": 1,
            "fullname": "Hello",
            "name": "World",
            "email": "hello@world.it",
            "gender": "Female",
            "dateBirth": None,
            "openToRecruiting": False,
            "openToNewsletter": True,
            "country": "United Kingdom",
            "isActive": True,
            "isStaff": False,
        },
    ]
    with patch("httpx.AsyncClient.post") as post_mock:
        post_mock.return_value = MockResponse(mock_data)

        response = await Client().users()

        assert response == mock_data
