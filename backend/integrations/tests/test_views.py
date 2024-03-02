from conferences.tests.factories import ConferenceFactory
from django.urls import reverse
from grants.models import Grant
from grants.tests.factories import GrantFactory
from integrations.plain_cards import _grant_status_to_color
import pytest
from users.tests.factories import UserFactory
from django.test import override_settings

pytestmark = pytest.mark.django_db


@override_settings(PLAIN_INTEGRATION_TOKEN="secret")
def test_cannot_get_plain_customer_cards_with_wrong_auth(rest_api_client):
    rest_api_client.token_auth("different")
    response = rest_api_client.post(
        reverse("plain_customer_cards"),
        {
            "cardKeys": ["grant"],
            "customer": {
                "email": "jane@example.org",
                "externalId": None,
            },
        },
        headers={
            "Conference-Id": "3",
        },
    )
    assert response.status_code == 401


@override_settings(PLAIN_INTEGRATION_TOKEN="secret")
def test_cannot_get_plain_customer_cards_with_missing_auth(rest_api_client):
    response = rest_api_client.post(
        reverse("plain_customer_cards"),
        {
            "cardKeys": ["grant"],
            "customer": {
                "email": "jane@example.org",
                "externalId": None,
            },
        },
        headers={
            "Conference-Id": "3",
        },
    )
    assert response.status_code == 401


@override_settings(PLAIN_INTEGRATION_TOKEN="secret")
def test_cannot_get_plain_customer_cards_when_user_doesnt_exist(rest_api_client):
    conference = ConferenceFactory()
    rest_api_client.token_auth("secret")

    response = rest_api_client.post(
        reverse("plain_customer_cards"),
        {
            "cardKeys": ["grant"],
            "customer": {
                "email": "jane@example.org",
                "externalId": None,
            },
        },
        headers={
            "Conference-Id": conference.id,
        },
    )

    assert response.status_code == 404


@override_settings(PLAIN_INTEGRATION_TOKEN="secret")
def test_cannot_get_plain_customer_cards_when_conference_doesnt_exist(rest_api_client):
    user = UserFactory()
    rest_api_client.token_auth("secret")

    response = rest_api_client.post(
        reverse("plain_customer_cards"),
        {
            "cardKeys": ["grant"],
            "customer": {
                "email": user.email,
                "externalId": None,
            },
        },
        headers={
            "Conference-Id": "3",
        },
    )

    assert response.status_code == 404


@override_settings(PLAIN_INTEGRATION_TOKEN="secret")
def test_get_plain_customer_cards_with_no_data(rest_api_client):
    conference = ConferenceFactory()
    user = UserFactory()

    rest_api_client.token_auth("secret")
    response = rest_api_client.post(
        reverse("plain_customer_cards"),
        {
            "cardKeys": ["grant"],
            "customer": {
                "email": user.email,
                "externalId": None,
            },
        },
        headers={
            "Conference-Id": conference.id,
        },
    )

    assert response.status_code == 200
    assert response.data["cards"] == [{"key": "grant", "components": []}]


@override_settings(PLAIN_INTEGRATION_TOKEN="secret")
def test_get_plain_customer_cards_grant_card(rest_api_client):
    user = UserFactory()
    grant = GrantFactory(
        user=user,
        approved_type=Grant.ApprovedType.ticket_travel_accommodation,
        travel_amount=100,
    )
    conference_id = grant.conference_id
    rest_api_client.token_auth("secret")
    response = rest_api_client.post(
        reverse("plain_customer_cards"),
        {
            "cardKeys": ["grant"],
            "customer": {
                "email": user.email,
                "externalId": None,
            },
        },
        headers={
            "Conference-Id": conference_id,
        },
    )

    assert response.status_code == 200
    data = response.data
    grant_card = next(card for card in data["cards"] if card["key"] == "grant")
    assert (
        grant_card["components"][0]["componentRow"]["rowMainContent"][0][
            "componentText"
        ]["text"]
        == "Status"
    )
    assert (
        grant_card["components"][0]["componentRow"]["rowAsideContent"][0][
            "componentBadge"
        ]["badgeLabel"]
        == grant.get_status_display()
    )

    assert (
        grant_card["components"][2]["componentRow"]["rowAsideContent"][0][
            "componentText"
        ]["text"]
        == grant.get_approved_type_display()
    )

    assert (
        grant_card["components"][4]["componentRow"]["rowAsideContent"][0][
            "componentText"
        ]["text"]
        == "€100.00"
    )


@override_settings(PLAIN_INTEGRATION_TOKEN="secret")
def test_get_plain_customer_cards_grant_card_with_no_travel(rest_api_client):
    user = UserFactory()
    grant = GrantFactory(
        user=user,
        approved_type=Grant.ApprovedType.ticket_only,
        travel_amount=100,
    )
    conference_id = grant.conference_id
    rest_api_client.token_auth("secret")
    response = rest_api_client.post(
        reverse("plain_customer_cards"),
        {
            "cardKeys": ["grant"],
            "customer": {
                "email": user.email,
                "externalId": None,
            },
        },
        headers={
            "Conference-Id": conference_id,
        },
    )

    assert response.status_code == 200
    data = response.data
    grant_card = next(card for card in data["cards"] if card["key"] == "grant")
    assert (
        grant_card["components"][0]["componentRow"]["rowMainContent"][0][
            "componentText"
        ]["text"]
        == "Status"
    )
    assert (
        grant_card["components"][0]["componentRow"]["rowAsideContent"][0][
            "componentBadge"
        ]["badgeLabel"]
        == grant.get_status_display()
    )

    assert (
        grant_card["components"][2]["componentRow"]["rowAsideContent"][0][
            "componentText"
        ]["text"]
        == grant.get_approved_type_display()
    )

    assert "Travel amount" not in str(grant_card)


@pytest.mark.parametrize(
    "status, expected_color",
    [
        (Grant.Status.pending, "GREY"),
        (Grant.Status.approved, "GREEN"),
        (Grant.Status.rejected, "RED"),
        (Grant.Status.waiting_list, "YELLOW"),
        (Grant.Status.waiting_list_maybe, "YELLOW"),
        (Grant.Status.waiting_for_confirmation, "BLUE"),
    ],
)
def test_grant_status_to_color(status, expected_color):
    assert _grant_status_to_color(status) == expected_color
