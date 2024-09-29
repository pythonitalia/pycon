import pytest
from notifications.models import EmailTemplateIdentifier
from django.urls import reverse

from django.contrib.admin.sites import AdminSite
from notifications.tests.factories import SentEmailFactory
from notifications.models import SentEmail
from notifications.admin.admins import SentEmailAdmin


def test_cannot_change_sent_email(rf):
    admin = SentEmailAdmin(
        model=SentEmail,
        admin_site=AdminSite(),
    )

    request = rf.get("/")
    assert admin.has_change_permission(request) is False
    assert admin.has_change_permission(request, SentEmailFactory()) is False
    assert admin.has_add_permission(request) is False


def test_get_view_on_site_url():
    admin = SentEmailAdmin(
        model=SentEmail,
        admin_site=AdminSite(),
    )

    sent_email = SentEmailFactory()
    assert not admin.get_view_on_site_url(None)
    assert admin.get_view_on_site_url(sent_email) == reverse(
        "admin:view-sent-email", args=[sent_email.id]
    )


def test_sent_email_admin_queryset(rf, admin_user):
    sent_email = SentEmailFactory(
        email_template__identifier=EmailTemplateIdentifier.custom,
        email_template__name="Custom template",
    )

    admin = SentEmailAdmin(
        model=SentEmail,
        admin_site=AdminSite(),
    )

    request = rf.get("/")
    request.user = admin_user
    qs = admin.get_queryset(request)

    assert qs.first().email_template.name == sent_email.email_template.name


@pytest.mark.parametrize("is_superuser", [True, False])
def test_sent_email_admin_only_superusers_can_see_system_emails(
    rf, admin_user, is_superuser
):
    sent_email = SentEmailFactory(
        email_template__conference=None,
        email_template__identifier=EmailTemplateIdentifier.reset_password,
        email_template__is_system_template=True,
        email_template__name="System email",
    )

    admin = SentEmailAdmin(
        model=SentEmail,
        admin_site=AdminSite(),
    )
    request = rf.get("/")
    request.user = admin_user
    request.user.is_superuser = is_superuser
    qs = admin.get_queryset(request)

    if is_superuser:
        assert qs.first().id == sent_email.id
    else:
        assert qs.first() is None


def test_email_template_display_name():
    admin = SentEmailAdmin(
        model=SentEmail,
        admin_site=AdminSite(),
    )

    sent_email = SentEmailFactory(
        email_template__identifier=EmailTemplateIdentifier.custom,
        email_template__name="Custom template",
    )
    visible_name = admin.email_template_display_name(sent_email)

    assert visible_name == sent_email.email_template.name

    sent_email = SentEmailFactory(
        email_template__identifier=EmailTemplateIdentifier.proposal_accepted,
        email_template__name="",
    )
    visible_name = admin.email_template_display_name(sent_email)

    assert visible_name == sent_email.email_template.get_identifier_display()
