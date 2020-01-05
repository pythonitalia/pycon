import pytest
from django.urls import reverse

NEWSLETTER_EMAIL_URL = "admin:newsletters_email_changelist"


@pytest.fixture
def post_changelist(admin_client, admin_user):
    admin_client.force_login(admin_user)

    def wrapper(**kwargs):
        resp = admin_client.post(reverse(NEWSLETTER_EMAIL_URL), kwargs)
        return resp

    return wrapper


@pytest.mark.django_db
def test_send_email(email_factory, subscription_factory, post_changelist):
    subscription_factory.create_batch(5)
    email = email_factory()
    resp = post_changelist(action="send_emails", _selected_action=[email.pk])
    assert resp.status_code == 302


@pytest.mark.django_db
def test_send_email_failed(email_factory, mocker, post_changelist):
    email = email_factory()
    send_email_mock = mocker.patch("notifications.emails.send_mail")
    send_email_mock.return_value = 0

    resp = post_changelist(action="send_emails", _selected_action=[email.pk])
    assert resp.status_code == 302
