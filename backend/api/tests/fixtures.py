import dataclasses
import json
from typing import Any, Dict, Optional
from conferences.tests.factories import ConferenceFactory
from datetime import date, time
import pytest
from django.test import Client as DjangoTestClient
from schedule.models import DayRoomThroughModel
from schedule.tests.factories import DayFactory, RoomFactory, SlotFactory
from wagtail.models import Locale
from wagtail.coreutils import get_supported_content_language_variant
from django.conf import settings


def query_wrapper(original):
    def call(*args, **kwargs):
        response = original(*args, **kwargs)
        response_dict = dataclasses.asdict(response)

        if response_dict.get("errors") is None:
            response_dict.pop("errors")

        return response_dict

    return call


# GraphQLClient.query = query_wrapper(async_to_sync(GraphQLClient.query))


class DjangoAsyncClientWrapper:
    def __init__(self, client) -> None:
        self.client = client

    async def post(self, *args, **kwargs):
        headers = kwargs.pop("headers", {})
        data = json.dumps(kwargs.pop("json"))
        content_type = "application/json"
        return await self.client.post(
            *args, data=data, content_type=content_type, **kwargs, **headers
        )


class NewGraphQLClient:
    GRAPHQL_URL = "/graphql"

    def __init__(self, *, include_full_response: bool = False):
        self.client = DjangoTestClient()
        self.include_full_response = include_full_response

    def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        body = {"query": query}
        headers = headers or {}

        if variables:
            body["variables"] = variables

        resp = self.client.post(
            self.GRAPHQL_URL,
            data=body,
            headers=headers,
            content_type="application/json",
        )
        data = json.loads(resp.content.decode())

        if self.include_full_response:
            return data, resp
        return data

    def force_login(self, user):
        self.client.force_login(user)


class AdminGraphQLAPIClient(NewGraphQLClient):
    GRAPHQL_URL = "/admin/graphql"


@pytest.fixture()
def graphql_client():
    return NewGraphQLClient()


@pytest.fixture()
def admin_graphql_api_client():
    return AdminGraphQLAPIClient()


@pytest.fixture()
def full_response_graphql_client():
    return NewGraphQLClient(include_full_response=True)


@pytest.fixture(autouse=True)
def create_languages(db):
    from languages.models import Language
    from languages.languages import LANGUAGES

    for language in LANGUAGES:
        Language.objects.create(name=language["English"], code=language["alpha2"])

    Locale.objects.create(
        language_code=get_supported_content_language_variant(settings.LANGUAGE_CODE),
    )


@pytest.fixture
def conference_with_schedule_setup():
    room_a = RoomFactory(name="Room A")
    room_b = RoomFactory(name="Room B")

    conference = ConferenceFactory()
    day_apr1 = DayFactory(
        day=date(2024, 4, 1),
        conference=conference,
    )

    DayRoomThroughModel.objects.create(day=day_apr1, room=room_a)
    DayRoomThroughModel.objects.create(day=day_apr1, room=room_b)

    SlotFactory(
        day=day_apr1,
        hour=time(9, 0),
        duration=30,
    )
    SlotFactory(
        day=day_apr1,
        hour=time(9, 30),
        duration=30,
    )
    SlotFactory(
        day=day_apr1,
        hour=time(10, 0),
        duration=30,
    )
    return conference
