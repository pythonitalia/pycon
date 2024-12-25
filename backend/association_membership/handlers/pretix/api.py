import urllib.parse
from typing import Literal

import requests

from django.conf import settings

from conferences.models.conference import Conference

METHODS = Literal["get", "post", "put", "patch", "delete"]


class PretixAPI:
    def __init__(self, organizer: str, event: str):
        self.organizer = organizer
        self.event = event
        self.base_url = (
            f"{settings.PRETIX_API}organizers/{self.organizer}/events/{self.event}"
        )

    @classmethod
    def for_conference(cls, conference: Conference):
        return cls(
            organizer=conference.pretix_organizer_id,
            event=conference.pretix_event_id,
        )

    def run_request(
        self,
        url: str,
        *,
        method: METHODS = "get",
        qs: dict[str, str] = None,
        json: dict = None,
    ):
        headers = {"Authorization": f"Token {str(settings.PRETIX_API_TOKEN)}"}

        if qs:
            url = f"{url}?" + "&".join([f"{key}={value}" for key, value in qs.items()])

        return getattr(requests, method)(url, headers=headers, json=json)

    def _request(self, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint}/"
        response = self.run_request(url, **kwargs)
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

    def get_all_attendee_tickets(self, attendee_email: str) -> list[dict]:
        response = self._request(
            "tickets/attendee-tickets",
            qs={"attendee_email": urllib.parse.quote_plus(attendee_email)},
        )
        return response.json()

    def has_attendee_ticket(
        self, attendee_email: str, additional_events: list[dict] = None
    ) -> bool:
        additional_events = additional_events or []
        events = [
            {
                "organizer_slug": self.organizer,
                "event_slug": self.event,
            }
        ] + additional_events

        response = self._request(
            "tickets/attendee-has-ticket",
            method="post",
            json={
                "attendee_email": attendee_email,
                "events": events,
            },
        )

        data = response.json()
        return data["user_has_admission_ticket"]
