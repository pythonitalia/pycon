import pytest
from django.contrib.admin.sites import AdminSite
from django.urls import reverse
from newsletters.admin import EmailAdmin
from newsletters.models import Email

NEWSLETTER_EMAIL_URL = "admin:newsletters_email_changelist"


@pytest.fixture
def post_changelist(admin_client, admin_user):
    admin_client.force_login(admin_user)

    def wrapper(**kwargs):
        resp = admin_client.post(reverse(NEWSLETTER_EMAIL_URL), kwargs)
        return resp

    return wrapper


@pytest.fixture
def post_send_email(admin_client, admin_user):
    admin_client.force_login(admin_user)

    def wrapper(pk, **kwargs):
        resp = admin_client.post(reverse("admin:send_email", args=[pk]), kwargs)
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


@pytest.mark.django_db
def test_send_single(email_factory, post_send_email):
    email = email_factory()
    resp = post_send_email(email.pk)
    assert resp.status_code == 302


@pytest.mark.django_db
def test_actions(email_factory):
    admin = EmailAdmin(Email, AdminSite())

    email = email_factory()
    assert (
        admin.email_actions(email)
        == f"""<a class="button" href="/admin/newsletters/email/{email.pk}/send_email/">Send Now!!</a>&nbsp;"""  # noqa
    )
