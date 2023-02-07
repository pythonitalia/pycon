from datetime import timedelta

import pytest
from django.utils import timezone

from grants.admin import send_reply_emails
from grants.models import Grant

pytestmark = pytest.mark.django_db


def test_send_reply_emails_approved_grant_missing_approved_type(
    rf, grant_factory, mocker
):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(status=Grant.Status.approved, approved_type=None)
    request = rf.get("/")

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.error.assert_called_once_with(
        request,
        f"Grant for {grant.name} is missing 'Grant Approved Type'!",
    )


def test_send_reply_emails_approved_missing_amount(rf, grant_factory, mocker):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.approved,
        approved_type=Grant.ApprovedType.ticket_accommodation,
        total_amount=None,
    )
    request = rf.get("/")

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.error.assert_called_once_with(
        request,
        f"Grant for {grant.name} is missing 'Approved Amount'!",
    )


def test_send_reply_emails_approved_set_deadline_in_fourteen_days(
    rf, grant_factory, mocker
):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.approved,
        approved_type=Grant.ApprovedType.ticket_accommodation,
        total_amount=800,
    )
    request = rf.get("/")

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.info.assert_called_once_with(
        request,
        f"Sent Approved reply email to {grant.name}",
    )

    grant.refresh_from_db()
    assert (
        f"{grant.applicant_reply_deadline:%Y-%m-%d}"
        == f"{(timezone.now().date() + timedelta(days=14)):%Y-%m-%d}"
    )


def test_send_reply_emails_waiting_list(rf, grant_factory, mocker):

    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.waiting_list,
    )
    request = rf.get("/")

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.info.assert_called_once_with(
        request, f"Sent Waiting List reply email to {grant.name}"
    )


def test_send_reply_emails_waiting_list_maybe(rf, grant_factory, mocker):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.waiting_list_maybe,
    )
    request = rf.get("/")

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.info.assert_called_once_with(
        request, f"Sent Waiting List reply email to {grant.name}"
    )


def test_send_reply_emails_waiting_list_already_sent_should_skip(
    rf, grant_factory, mocker
):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.waiting_list, applicant_reply_sent_at=timezone.now()
    )
    request = rf.get("/")

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.warning.assert_called_once_with(
        request,
        f"Reply email for {grant.name} was already sent! Skipping.",
    )


def test_send_reply_emails_waiting_list_maybe_already_sent_should_skip(
    rf, grant_factory, mocker
):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.waiting_list_maybe, applicant_reply_sent_at=timezone.now()
    )
    request = rf.get("/")

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.warning.assert_called_once_with(
        request,
        f"Reply email for {grant.name} was already sent! Skipping.",
    )


def test_send_reply_emails_rejected(rf, grant_factory, mocker):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.rejected,
    )
    request = rf.get("/")

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.info.assert_called_once_with(
        request, f"Sent Rejected reply email to {grant.name}"
    )


def test_send_reply_emails_rejected_already_sent_should_skip(rf, grant_factory, mocker):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.rejected, applicant_reply_sent_at=timezone.now()
    )
    request = rf.get("/")

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.warning.assert_called_once_with(
        request,
        f"Reply email for {grant.name} was already sent! Skipping.",
    )
