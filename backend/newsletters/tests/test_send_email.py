import pytest
from django.urls import reverse

NEWSLETTER_CHANGELIST_URL = "admin:newsletters_subscription_changelist"


@pytest.fixture
def post_changelist(admin_client, admin_user):
    admin_client.force_login(admin_user)

    def wrapper(**kwargs):
        resp = admin_client.post(reverse(NEWSLETTER_CHANGELIST_URL), kwargs)
        return resp

    return wrapper


@pytest.mark.django_db
def test_get_email_form(admin_client, admin_user):
    admin_client.force_login(admin_user)
    resp = admin_client.get(reverse(NEWSLETTER_CHANGELIST_URL), {})
    assert resp.status_code == 200
    assert resp.context_data["submitted"] is False
    assert resp.context_data.get("form")


@pytest.mark.django_db
def test_submit_valid_email_form(post_changelist):
    data = {
        "subject": "My Subject",
        "body": "My Body",
        "recipients_types": "newsletter",
    }
    resp = post_changelist(**data)
    assert resp.status_code == 200
    assert resp.context_data["submitted"] is True
    assert not resp.context_data["form"].errors


@pytest.mark.django_db
def test_submit_invalid_email_form(post_changelist):
    resp = post_changelist()
    assert resp.status_code == 200
    assert resp.context_data["submitted"] is False
    assert resp.context_data["form"].errors


@pytest.mark.django_db
def test_send_newsletter(post_changelist, subscription_factory):

    sub1 = subscription_factory()
    sub2 = subscription_factory()

    data = {
        "subject": "My Subject",
        "body": "My Body",
        "recipients_types": "newsletter",
    }
    resp = post_changelist(**data)
    assert resp.status_code == 200

    assert resp.context_data["submitted"] is True
    assert resp.context_data["form"].cleaned_data["recipients"] == [
        sub1.email,
        sub2.email,
    ]


@pytest.mark.django_db
def test_recipients_type_not_valid(post_changelist):
    data = {"subject": "My Subject", "body": "My Body", "recipients_types": "booooohhh"}
    resp = post_changelist(**data)
    assert resp.status_code == 200
    assert resp.context_data["submitted"] is False
    assert resp.context_data["form"].errors["recipients_types"] == [
        "Select a valid choice. booooohhh is not one of the available choices."
    ]
