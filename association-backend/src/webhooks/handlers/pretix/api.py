from typing import Literal

import httpx

from src.association.settings import PRETIX_API_TOKEN, PRETIX_API_URL

METHODS = Literal["get"]


class PretixAPI:
    def __init__(self, organizer: str, event: str):
        self.organizer = organizer
        self.event = event
        self.base_url = (
            f"{PRETIX_API_URL}organizers/{self.organizer}/events/{self.event}"
        )

    def _request(self, endpoint: str, method: METHODS = "get"):
        url = f"{self.base_url}/{endpoint}/"
        headers = {"Authorization": f"Token {str(PRETIX_API_TOKEN)}"}

        with httpx.Client(headers=headers) as client:
            response = getattr(client, method)(url)

        response.raise_for_status()
        return response

    def get_order_data(self, order_code: str) -> dict:
        response = self._request(f"orders/{order_code}")
        return response.json()

    def get_item_data(self, item_id: str) -> dict:
        response = self._request(f"items/{item_id}")
        return response.json()

    def get_categories(self) -> dict:
        response = self._request("categories")
        return response.json()
