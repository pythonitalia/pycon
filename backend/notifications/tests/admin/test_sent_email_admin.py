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


def test_send_email_action(rf, admin_user, django_capture_on_commit_callbacks, mocker):
    mock_send_pending_email = mocker.patch(
        "notifications.admin.admins.send_pending_email.delay"
    )
    admin = SentEmailAdmin(
        model=SentEmail,
        admin_site=AdminSite(),
    )
    admin.message_user = mocker.Mock()

    request = rf.post("/")
    request.user = admin_user

    draft_email_1 = SentEmailFactory(status=SentEmail.Status.draft)
    draft_email_2 = SentEmailFactory(status=SentEmail.Status.draft)
    pending_email = SentEmailFactory(status=SentEmail.Status.pending)
    sent_email = SentEmailFactory(status=SentEmail.Status.sent)
    failed_email = SentEmailFactory(status=SentEmail.Status.failed)

    with django_capture_on_commit_callbacks(execute=True):
        admin.send_email(request, SentEmail.objects.all())

    # drafts, pending and failed emails are all (re)queued for sending
    queued_ids = {call.args[0] for call in mock_send_pending_email.call_args_list}
    assert queued_ids == {
        draft_email_1.id,
        draft_email_2.id,
        pending_email.id,
        failed_email.id,
    }
    assert mock_send_pending_email.call_count == 4

    for email in (draft_email_1, draft_email_2, pending_email, failed_email):
        email.refresh_from_db()
        assert email.status == SentEmail.Status.pending

    # already sent emails are never touched
    sent_email.refresh_from_db()
    assert sent_email.status == SentEmail.Status.sent

    admin.message_user.assert_called_once_with(request, "Emails queued for sending: 4")


def test_send_email_action_with_a_status_filtered_queryset(
    rf, admin_user, django_capture_on_commit_callbacks, mocker
):
    """The changelist queryset carries the active list_filter, so the action
    receives a queryset already narrowed to a single status."""
    mock_send_pending_email = mocker.patch(
        "notifications.admin.admins.send_pending_email.delay"
    )
    admin = SentEmailAdmin(
        model=SentEmail,
        admin_site=AdminSite(),
    )
    admin.message_user = mocker.Mock()

    request = rf.post("/")
    request.user = admin_user

    draft_email = SentEmailFactory(status=SentEmail.Status.draft)

    with django_capture_on_commit_callbacks(execute=True):
        admin.send_email(
            request, SentEmail.objects.filter(status=SentEmail.Status.draft)
        )

    mock_send_pending_email.assert_called_once_with(draft_email.id)

    draft_email.refresh_from_db()
    assert draft_email.status == SentEmail.Status.pending


def test_send_email_action_keeps_queueing_after_a_broker_failure(
    rf, admin_user, django_capture_on_commit_callbacks, mocker
):
    mock_send_pending_email = mocker.patch(
        "notifications.admin.admins.send_pending_email.delay",
        side_effect=[Exception("broker is down"), None],
    )
    admin = SentEmailAdmin(
        model=SentEmail,
        admin_site=AdminSite(),
    )
    admin.message_user = mocker.Mock()

    request = rf.post("/")
    request.user = admin_user

    SentEmailFactory(status=SentEmail.Status.draft)
    SentEmailFactory(status=SentEmail.Status.draft)

    with django_capture_on_commit_callbacks(execute=True):
        admin.send_email(request, SentEmail.objects.all())

    # the first publish blowing up must not strand the remaining emails
    assert mock_send_pending_email.call_count == 2
