from typing import Literal

import httpx

from django.conf import settings

METHODS = Literal["get"]


class PretixAPI:
    def __init__(self, organizer: str, event: str):
        self.organizer = organizer
        self.event = event
        self.base_url = (
            f"{settings.PRETIX_API}organizers/{self.organizer}/events/{self.event}"
        )

    def _request(
        self, endpoint: str, *, method: METHODS = "get", qs: dict[str, str] = None
    ):
        url = f"{self.base_url}/{endpoint}/"
        headers = {"Authorization": f"Token {str(settings.PRETIX_API_TOKEN)}"}

        if qs:
            url = f"{url}?" + "&".join([f"{key}={value}" for key, value in qs.items()])

        with httpx.Client(headers=headers) as client:
            response = getattr(client, method)(url)

        response.raise_for_status()
        return response

    def get_order_data(self, order_code: str) -> dict:
        response = self._request(f"orders/{order_code}")
        return response.json()

    def get_items(self, qs: dict[str, str]) -> dict:
        response = self._request("items", qs=qs)
        return response.json()

    def get_categories(self) -> dict:
        response = self._request("categories")
        return response.json()
