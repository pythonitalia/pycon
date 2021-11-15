import pytest
from django.test.utils import override_settings

from integrations.mailchimp import MailchimpError, subscribe


@override_settings(MAILCHIMP_SECRET_KEY="")
def test_mailchimp_not_configure():
    with pytest.raises(ValueError, match="Mailchimp integration is not configured"):
        subscribe("me@pycon.it")


@override_settings(MAILCHIMP_LIST_ID="1234")
def test_subscribe_mailchimp_success_response(requests_mock):
    requests_mock.post(
        "https://us5.api.mailchimp.com/3.0/lists/1234/members",
        json={
            "email_address": "sushi@pycon.it",
            "status": "subscribed",
            "id": "63b71566-4658-11ec-81d3-0242ac130003",
        },
    )

    resp = subscribe("sushi@pycon.it")

    assert resp is True


@override_settings(MAILCHIMP_LIST_ID="1234")
def test_subscribe_mailchimp_already_exists(requests_mock):
    requests_mock.post(
        "https://us5.api.mailchimp.com/3.0/lists/1234/members",
        json={
            "title": "Member Exists",
            "status": 400,
            "detail": "pizza@pycon.it is already a list member. Use PUT to insert or update list members.",
            "instance": "59588eec-4658-11ec-81d3-0242ac130003",
        },
    )

    resp = subscribe("pizza@pycon.it")

    assert resp is True


@override_settings(MAILCHIMP_LIST_ID="1234")
def test_subscribe_mailchimp_error_response(requests_mock):
    requests_mock.post(
        "https://us5.api.mailchimp.com/3.0/lists/1234/members",
        json={
            "type": "https://mailchimp.com/developer/marketing/docs/errors/",
            "title": "Resource Not Found",
            "status": 404,
            "detail": "The requested resource could not be found.",
            "instance": "b49b2842-f1fc-25c6-135b-d8204fe18b10",
        },
    )

    with pytest.raises(
        MailchimpError,
        match="404 Resource Not Found: The requested resource could not be found.",
    ):
        subscribe("pizza@pycon.it")
