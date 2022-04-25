import pytest

from integrations.mailchimp import SubscriptionResult, subscribe

SUSHI_AT_PYCON_MD5 = "b18048f470386b1e7b7f4500d1251d36"


def test_mailchimp_not_configure(settings):
    settings.MAILCHIMP_SECRET_KEY = ""
    with pytest.raises(ValueError, match="Mailchimp integration is not configured"):
        subscribe("me@pycon.it")


def test_subscribe_with_not_existent_email(settings, requests_mock):
    settings.MAILCHIMP_LIST_ID = "1234"
    settings.MAILCHIMP_DC = "us5"

    requests_mock.get(
        f"https://us5.api.mailchimp.com/3.0/lists/1234/members/{SUSHI_AT_PYCON_MD5}",
        status_code=404,
    )
    requests_mock.put(
        f"https://us5.api.mailchimp.com/3.0/lists/1234/members/{SUSHI_AT_PYCON_MD5}",
        json={
            "email_address": "sushi@pycon.it",
            "status_if_new": "subscribed",
            "status": "subscribed",
        },
    )

    resp = subscribe("sushi@pycon.it")

    assert resp == SubscriptionResult.SUBSCRIBED


def test_subscribe_with_existing_email(settings, requests_mock):
    settings.MAILCHIMP_LIST_ID = "1234"
    settings.MAILCHIMP_DC = "us5"

    requests_mock.get(
        f"https://us5.api.mailchimp.com/3.0/lists/1234/members/{SUSHI_AT_PYCON_MD5}",
        status_code=200,
        json={"status": "subscribed"},
    )
    requests_mock.put(
        f"https://us5.api.mailchimp.com/3.0/lists/1234/members/{SUSHI_AT_PYCON_MD5}",
        json={
            "email_address": "sushi@pycon.it",
            "status_if_new": "subscribed",
            "status": "subscribed",
        },
    )

    resp = subscribe("sushi@pycon.it")

    assert resp == SubscriptionResult.SUBSCRIBED


def test_subscribe_when_unsubscribed(settings, requests_mock):
    settings.MAILCHIMP_LIST_ID = "1234"
    settings.MAILCHIMP_DC = "us5"

    requests_mock.get(
        f"https://us5.api.mailchimp.com/3.0/lists/1234/members/{SUSHI_AT_PYCON_MD5}",
        status_code=200,
        json={"status": "unsubscribed"},
    )
    requests_mock.put(
        f"https://us5.api.mailchimp.com/3.0/lists/1234/members/{SUSHI_AT_PYCON_MD5}",
        json={
            "email_address": "sushi@pycon.it",
            "status_if_new": "subscribed",
            "status": "pending",
        },
    )

    resp = subscribe("sushi@pycon.it")

    assert resp == SubscriptionResult.WAITING_CONFIRMATION


def test_subscribe_when_still_pending(settings, requests_mock):
    settings.MAILCHIMP_LIST_ID = "1234"
    settings.MAILCHIMP_DC = "us5"

    requests_mock.get(
        f"https://us5.api.mailchimp.com/3.0/lists/1234/members/{SUSHI_AT_PYCON_MD5}",
        status_code=200,
        json={"status": "pending"},
    )
    requests_mock.put(
        f"https://us5.api.mailchimp.com/3.0/lists/1234/members/{SUSHI_AT_PYCON_MD5}",
        json={
            "email_address": "sushi@pycon.it",
            "status_if_new": "subscribed",
            "status": "pending",
        },
    )

    resp = subscribe("sushi@pycon.it")

    assert resp == SubscriptionResult.WAITING_CONFIRMATION
