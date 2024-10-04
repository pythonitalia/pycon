from unittest.mock import patch

from privacy_policy.models import PrivacyPolicyAcceptanceRecord
from conferences.tests.factories import ConferenceFactory
from users.tests.factories import UserFactory
import pytest
from pytest import mark

from integrations.flodesk import SubscriptionResult
from newsletters.models import Subscription
import requests


def test_subscribe_to_newsletter(graphql_client):
    conference = ConferenceFactory()
    email = "me@example.it"
    variables = {"email": email, "conferenceCode": conference.code}

    query = """
        mutation($input: SubscribeToNewsletterInput!) {
            subscribeToNewsletter(input: $input) {
            __typename

            ... on NewsletterSubscribeResult {
                status
            }
        }
    }
    """

    with patch(
        "api.newsletters.mutations.subscribe_to_newsletter.subscribe"
    ) as mock_subscription:
        mock_subscription.return_value = SubscriptionResult.SUBSCRIBED

        resp = graphql_client.query(query, variables={"input": variables})

    assert (
        resp["data"]["subscribeToNewsletter"]["__typename"]
        == "NewsletterSubscribeResult"
    )
    assert resp["data"]["subscribeToNewsletter"]["status"] == "SUBSCRIBED"

    assert PrivacyPolicyAcceptanceRecord.objects.filter(
        user=None, email=email, conference=conference, privacy_policy="newsletter"
    ).exists()


@pytest.mark.parametrize(
    "exception",
    [
        requests.exceptions.HTTPError(response=requests.Response()),
        ValueError("exception"),
    ],
)
def test_subscribe_to_newsletter_fails_on_api_side(graphql_client, exception):
    conference = ConferenceFactory()
    email = "me@example.it"
    variables = {"email": email, "conferenceCode": conference.code}

    query = """
        mutation($input: SubscribeToNewsletterInput!) {
            subscribeToNewsletter(input: $input) {
            __typename

            ... on NewsletterSubscribeResult {
                status
            }
        }
    }
    """

    with patch(
        "api.newsletters.mutations.subscribe_to_newsletter.subscribe"
    ) as mock_subscription:
        mock_subscription.side_effect = exception

        resp = graphql_client.query(query, variables={"input": variables})

        assert (
            resp["data"]["subscribeToNewsletter"]["__typename"]
            == "NewsletterSubscribeResult"
        )
        assert resp["data"]["subscribeToNewsletter"]["status"] == "UNABLE_TO_SUBSCRIBE"


@pytest.mark.parametrize("email", ["", "me-invalid"])
def test_subscribe_to_newsletter_with_invalid_email_fails(graphql_client, email):
    conference = ConferenceFactory()
    variables = {"email": email, "conferenceCode": conference.code}

    query = """
        mutation($input: SubscribeToNewsletterInput!) {
            subscribeToNewsletter(input: $input) {
            __typename

            ... on SubscribeToNewsletterErrors {
                errors {
                    email
                }
            }
        }
    }
    """

    with patch(
        "api.newsletters.mutations.subscribe_to_newsletter.subscribe"
    ) as mock_subscription:
        mock_subscription.return_value = SubscriptionResult.SUBSCRIBED

        resp = graphql_client.query(query, variables={"input": variables})

        assert (
            resp["data"]["subscribeToNewsletter"]["__typename"]
            == "SubscribeToNewsletterErrors"
        )
        assert resp["data"]["subscribeToNewsletter"]["errors"]["email"] == [
            "Invalid email address"
        ]


@pytest.mark.parametrize("conference_code", ["", "invalid-conf"])
def test_subscribe_to_newsletter_with_invalid_conference_code(
    graphql_client, conference_code
):
    ConferenceFactory(code="valid")
    variables = {"email": "example@example.com", "conferenceCode": conference_code}

    query = """
        mutation($input: SubscribeToNewsletterInput!) {
            subscribeToNewsletter(input: $input) {
            __typename

            ... on SubscribeToNewsletterErrors {
                errors {
                    email
                    conferenceCode
                }
            }
        }
    }
    """

    with patch(
        "api.newsletters.mutations.subscribe_to_newsletter.subscribe"
    ) as mock_subscription:
        mock_subscription.return_value = SubscriptionResult.SUBSCRIBED
        resp = graphql_client.query(query, variables={"input": variables})

    assert (
        resp["data"]["subscribeToNewsletter"]["__typename"]
        == "SubscribeToNewsletterErrors"
    )
    assert resp["data"]["subscribeToNewsletter"]["errors"]["conferenceCode"] == [
        "Invalid conference code"
    ]


def _update_user_newsletter(graphql_client, user, open_to_newsletter):
    query = """
    mutation(
        $open_to_newsletter: Boolean!,
        $open_to_recruiting: Boolean!,
        $date_birth: String
    ){
        update(input: {
            openToNewsletter: $open_to_newsletter,
            openToRecruiting: $open_to_recruiting,
            dateBirth: $date_birth
        }){
            __typename
            ... on User {
                id
                openToNewsletter
            }
            ... on UpdateErrors {
                validationOpenToNewsletter: openToNewsletter
                nonFieldErrors
            }
        }
    }
    """
    variables = {
        "open_to_newsletter": open_to_newsletter,
        "open_to_recruiting": user.open_to_recruiting,
        "date_birth": f"{user.date_birth:%Y-%m-%d}",
    }
    return graphql_client.query(query=query, variables=variables), variables


@pytest.mark.skip
@mark.django_db
def test_subscribe_when_update_user(graphql_client):
    user = UserFactory(open_to_newsletter=False)
    graphql_client.force_login(user)

    resp, variables = _update_user_newsletter(graphql_client, user, True)

    assert resp["data"]["update"]["__typename"] == "MeUser"
    assert resp["data"]["update"]["openToNewsletter"] is True
    assert Subscription.objects.get(email=user.email)


@pytest.mark.skip
@mark.django_db
def test_unsubscribe_when_update_user(graphql_client):
    user = UserFactory(open_to_newsletter=True)
    graphql_client.force_login(user)

    resp, variables = _update_user_newsletter(graphql_client, user, False)

    assert resp["data"]["update"]["__typename"] == "MeUser"
    assert resp["data"]["update"]["openToNewsletter"] is False

    with pytest.raises(Subscription.DoesNotExist):
        Subscription.objects.get(email=user.email)
