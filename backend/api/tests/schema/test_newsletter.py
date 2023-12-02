from unittest.mock import patch

import pytest
from pytest import mark

from pycon.backend.integrations.flodesk import SubscriptionResult
from newsletters.models import Subscription


def test_subscribe_to_newsletter(graphql_client):
    email = "me@example.it"
    variables = {"email": email}

    query = """
        mutation($email: String!) {
            subscribeToNewsletter(input: {
                email: $email
            }) {
            __typename

            ... on NewsletterSubscribeResult {
                status
            }
        }
    }
    """

    with patch("api.newsletters.forms.subscribe") as mock_subscription:
        mock_subscription.return_value = SubscriptionResult.SUBSCRIBED

        resp = graphql_client.query(query, variables=variables)

        assert (
            resp["data"]["subscribeToNewsletter"]["__typename"]
            == "NewsletterSubscribeResult"
        )
        assert resp["data"]["subscribeToNewsletter"]["status"] == "SUBSCRIBED"


@pytest.mark.skip
@mark.django_db
def test_unsubscribe_not_registered_mail_to_newsletter(graphql_client):
    """If the mail is already unsubscribed (it's not in the subcription table)
    return true anyway"""

    email = "me@example.it"

    variables = {"email": email}

    query = """
            mutation($email: String!) {
                unsubscribeToNewsletter(input: {
                    email: $email
                }) {
                __typename

                ... on UnsubscribeToNewsletterErrors {
                    email
                }

                ... on NewsletterSubscribeResult {
                    status
                }
            }
        }
        """

    resp = graphql_client.query(query, variables=variables)

    assert resp["data"]["unsubscribeToNewsletter"]["status"] is True


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
def test_subscribe_when_update_user(graphql_client, user_factory):
    user = user_factory(open_to_newsletter=False)
    graphql_client.force_login(user)

    resp, variables = _update_user_newsletter(graphql_client, user, True)

    assert resp["data"]["update"]["__typename"] == "MeUser"
    assert resp["data"]["update"]["openToNewsletter"] is True
    assert Subscription.objects.get(email=user.email)


@pytest.mark.skip
@mark.django_db
def test_unsubscribe_when_update_user(graphql_client, user_factory):
    user = user_factory(open_to_newsletter=True)
    graphql_client.force_login(user)

    resp, variables = _update_user_newsletter(graphql_client, user, False)

    assert resp["data"]["update"]["__typename"] == "MeUser"
    assert resp["data"]["update"]["openToNewsletter"] is False

    with pytest.raises(Subscription.DoesNotExist):
        Subscription.objects.get(email=user.email)
