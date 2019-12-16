import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_email_form(admin_client, admin_user):
    admin_client.force_login(admin_user)
    resp = admin_client.get(reverse("admin:newsletters_subscription_changelist"), {})
    assert resp.status_code == 200
    assert resp.context_data["submitted"] is False
    assert resp.context_data.get("form")


@pytest.mark.django_db
def test_submit_valid_email_form(admin_client, admin_user):
    admin_client.force_login(admin_user)

    data = {"subject": "My Subject", "body": "My Body"}
    resp = admin_client.post(reverse("admin:newsletters_subscription_changelist"), data)
    assert resp.status_code == 200
    assert resp.context_data["submitted"] is True
    assert not resp.context_data["form"].errors


@pytest.mark.django_db
def test_submit_invalid_email_form(admin_client, admin_user):
    admin_client.force_login(admin_user)
    resp = admin_client.post(reverse("admin:newsletters_subscription_changelist"), {})
    assert resp.status_code == 200
    assert resp.context_data["submitted"] is False
    assert resp.context_data["form"].errors
