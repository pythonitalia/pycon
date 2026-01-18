from datetime import timedelta
from decimal import Decimal
from unittest.mock import call

import pytest
from django.contrib.admin.models import LogEntry
from django.contrib.admin.sites import AdminSite
from django.utils import timezone

from conferences.models.conference_voucher import ConferenceVoucher
from conferences.tests.factories import ConferenceFactory, ConferenceVoucherFactory
from grants.admin import (
    confirm_pending_status,
    GrantAdmin,
    GrantReimbursementAdmin,
    create_grant_vouchers,
    mark_rejected_and_send_email,
    reset_pending_status_back_to_status,
    send_grant_reminder_to_waiting_for_confirmation,
    send_reply_email_waiting_list_update,
    send_reply_emails,
)
from grants.tests.factories import (
    GrantFactory,
    GrantReimbursementFactory,
)
from grants.models import Grant, GrantReimbursement

pytestmark = pytest.mark.django_db


def test_send_reply_emails_with_grants_from_multiple_conferences_fails(
    rf, mocker, admin_user
):
    """
    Test that sending reply emails does not proceed when selected grants belong
    to different conferences and appropriately displays an error message.
    """
    mock_messages = mocker.patch("custom_admin.admin.messages")
    conference1 = ConferenceFactory()
    conference2 = ConferenceFactory()
    grant1 = GrantFactory(conference=conference1, status=Grant.Status.approved)
    grant2 = GrantFactory(conference=conference2, status=Grant.Status.waiting_list)
    grant3 = GrantFactory(conference=conference2, status=Grant.Status.rejected)
    request = rf.get("/")
    request.user = admin_user
    mock_send_approved_email = mocker.patch(
        "grants.admin.send_grant_reply_approved_email.delay"
    )
    mock_send_waiting_list_email = mocker.patch(
        "grants.admin.send_grant_reply_waiting_list_email.delay"
    )
    mock_send_rejected_email = mocker.patch(
        "grants.admin.send_grant_reply_rejected_email.delay"
    )

    send_reply_emails(
        None,
        request=request,
        queryset=Grant.objects.filter(id__in=[grant1.id, grant2.id, grant3.id]),
    )

    mock_messages.error.assert_called_once_with(
        request,
        "Please select only one conference",
    )
    mock_send_approved_email.assert_not_called()
    mock_send_waiting_list_email.assert_not_called()
    mock_send_rejected_email.assert_not_called()
    assert not LogEntry.objects.exists()


def test_send_reply_emails_approved_grant_missing_reimbursements(
    rf, mocker, admin_user
):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = GrantFactory(status=Grant.Status.approved)
    request = rf.get("/")
    request.user = admin_user
    mock_send_approved_email = mocker.patch(
        "grants.admin.send_grant_reply_approved_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.error.assert_called_once_with(
        request,
        f"Grant for {grant.name} is missing reimbursement categories!",
    )
    mock_send_approved_email.assert_not_called()
    assert not LogEntry.objects.exists()


def test_send_reply_emails_approved_missing_amount(rf, mocker, admin_user):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = GrantFactory(status=Grant.Status.approved)
    # Create reimbursement with 0 amount so total_allocated_amount is 0
    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__ticket=True,
        granted_amount=Decimal("0"),
    )
    request = rf.get("/")
    request.user = admin_user
    mock_send_approved_email = mocker.patch(
        "grants.admin.send_grant_reply_approved_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.error.assert_called_once_with(
        request,
        f"Grant for {grant.name} is missing 'Total Amount'!",
    )
    mock_send_approved_email.assert_not_called()
    assert not LogEntry.objects.exists()


def test_send_reply_emails_approved_set_deadline_in_fourteen_days(
    rf, mocker, admin_user
):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = GrantFactory(status=Grant.Status.approved)
    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__ticket=True,
        granted_amount=Decimal("100"),
    )
    GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__accommodation=True,
        category__max_amount=Decimal("700"),
        granted_amount=Decimal("700"),
    )
    request = rf.get("/")
    request.user = admin_user
    mock_send_approved_email = mocker.patch(
        "grants.admin.send_grant_reply_approved_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    # Verify admin action was called correctly
    mock_messages.info.assert_called_once_with(
        request,
        f"Sent Approved reply email to {grant.name}",
    )

    # Verify deadline was set correctly
    grant.refresh_from_db()
    assert (
        f"{grant.applicant_reply_deadline:%Y-%m-%d}"
        == f"{(timezone.now().date() + timedelta(days=14)):%Y-%m-%d}"
    )

    # Verify task was queued correctly
    mock_send_approved_email.assert_called_once_with(
        grant_id=grant.id, is_reminder=False
    )

    # Verify audit log entry was created correctly
    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant.id,
        change_message="Sent Approved reply email to applicant",
    ).exists()


def test_send_reply_emails_waiting_list(rf, mocker, admin_user):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = GrantFactory(
        status=Grant.Status.waiting_list,
    )
    request = rf.get("/")
    request.user = admin_user
    mock_send_waiting_list_email = mocker.patch(
        "grants.admin.send_grant_reply_waiting_list_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.info.assert_called_once_with(
        request, f"Sent Waiting List reply email to {grant.name}"
    )
    mock_send_waiting_list_email.assert_called_once_with(grant_id=grant.id)
    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant.id,
        change_message="Sent Waiting List reply email to applicant",
    ).exists()


def test_send_reply_emails_waiting_list_maybe(rf, mocker, admin_user):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = GrantFactory(
        status=Grant.Status.waiting_list_maybe,
    )
    request = rf.get("/")
    request.user = admin_user
    mock_send_waiting_list_email = mocker.patch(
        "grants.admin.send_grant_reply_waiting_list_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.info.assert_called_once_with(
        request, f"Sent Waiting List reply email to {grant.name}"
    )
    mock_send_waiting_list_email.assert_called_once_with(grant_id=grant.id)
    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant.id,
        change_message="Sent Waiting List reply email to applicant",
    ).exists()


def test_send_reply_emails_rejected(rf, mocker, admin_user):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = GrantFactory(
        status=Grant.Status.rejected,
    )
    request = rf.get("/")
    request.user = admin_user
    mock_send_rejected_email = mocker.patch(
        "grants.admin.send_grant_reply_rejected_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.info.assert_called_once_with(
        request, f"Sent Rejected reply email to {grant.name}"
    )
    mock_send_rejected_email.assert_called_once_with(grant_id=grant.id)
    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant.id,
        change_message="Sent Rejected reply email to applicant",
    ).exists()


def test_send_grant_reminder_to_waiting_for_confirmation(rf, mocker, admin_user):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = GrantFactory(status=Grant.Status.waiting_for_confirmation)
    request = rf.get("/")
    request.user = admin_user
    mock_send_approved_reminder_email = mocker.patch(
        "grants.admin.send_grant_reply_approved_email.delay"
    )

    send_grant_reminder_to_waiting_for_confirmation(
        None, request=request, queryset=Grant.objects.all()
    )

    # Verify admin action was called correctly
    mock_messages.info.assert_called_once_with(
        request,
        f"Grant reminder sent to {grant.name}",
    )

    # Verify task was queued correctly
    mock_send_approved_reminder_email.assert_called_once_with(
        grant_id=grant.id, is_reminder=True
    )

    # Verify audit log entry was created correctly
    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant.id,
        change_message="Sent Approved reminder email to applicant",
    ).exists()


def test_send_reply_email_waiting_list_update(rf, mocker, admin_user):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = GrantFactory(status=Grant.Status.waiting_list)
    request = rf.get("/")
    request.user = admin_user
    mock_send_waiting_list_update_email = mocker.patch(
        "grants.admin.send_grant_reply_waiting_list_update_email.delay"
    )

    send_reply_email_waiting_list_update(
        None, request=request, queryset=Grant.objects.all()
    )

    # Verify admin action was called correctly
    mock_messages.info.assert_called_once_with(
        request,
        f"Sent Waiting List update reply email to {grant.name}",
    )

    # Verify task was queued correctly
    mock_send_waiting_list_update_email.assert_called_once_with(grant_id=grant.id)

    # Verify audit log entry was created correctly
    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant.id,
        change_message="Sent Waiting List update reply email to applicant",
    ).exists()


def test_create_grant_vouchers(rf, mocker, admin_user):
    mock_messages = mocker.patch("grants.admin.messages")

    conference = ConferenceFactory()

    grant_1 = GrantFactory(
        status=Grant.Status.confirmed,
        conference=conference,
    )
    grant_2 = GrantFactory(
        status=Grant.Status.confirmed,
        conference=conference,
    )
    request = rf.get("/")
    request.user = admin_user

    create_grant_vouchers(
        None,
        request=request,
        queryset=Grant.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.count() == 2
    grant_1_voucher = ConferenceVoucher.objects.filter(user_id=grant_1.user_id).get()
    assert grant_1_voucher.voucher_type == ConferenceVoucher.VoucherType.GRANT
    assert grant_1_voucher.conference == conference

    grant_2_voucher = ConferenceVoucher.objects.filter(user_id=grant_2.user_id).get()
    assert grant_2_voucher.voucher_type == ConferenceVoucher.VoucherType.GRANT
    assert grant_2_voucher.conference == conference

    mock_messages.success.assert_called_once_with(
        request,
        "Vouchers created!",
    )
    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant_1.id,
        change_message="Created voucher for this grant",
    ).exists()
    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant_2.id,
        change_message="Created voucher for this grant",
    ).exists()


@pytest.mark.parametrize(
    "type", [ConferenceVoucher.VoucherType.SPEAKER, ConferenceVoucher.VoucherType.GRANT]
)
def test_create_grant_vouchers_with_existing_voucher_is_reused(
    rf, mocker, admin_user, type
):
    mock_messages = mocker.patch("grants.admin.messages")

    conference = ConferenceFactory()

    grant_1 = GrantFactory(
        status=Grant.Status.confirmed,
        conference=conference,
    )

    grant_1_voucher = ConferenceVoucherFactory(
        user=grant_1.user,
        conference=conference,
        voucher_type=type,
    )

    grant_2 = GrantFactory(
        status=Grant.Status.confirmed,
        conference=conference,
    )
    request = rf.get("/")
    request.user = admin_user

    create_grant_vouchers(
        None,
        request=request,
        queryset=Grant.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.count() == 2

    grant_1_voucher.refresh_from_db()
    assert grant_1_voucher.voucher_type == type
    assert grant_1_voucher.conference == conference

    grant_2_voucher = ConferenceVoucher.objects.filter(user_id=grant_2.user_id).get()
    assert grant_2_voucher.voucher_type == ConferenceVoucher.VoucherType.GRANT
    assert grant_2_voucher.conference == conference

    mock_messages.success.assert_called_once_with(
        request,
        "Vouchers created!",
    )


@pytest.mark.parametrize(
    "type", [ConferenceVoucher.VoucherType.SPEAKER, ConferenceVoucher.VoucherType.GRANT]
)
def test_create_grant_vouchers_with_voucher_from_other_conf_is_ignored(
    rf, mocker, type, admin_user
):
    mock_messages = mocker.patch("grants.admin.messages")

    conference = ConferenceFactory()
    other_conference = ConferenceFactory()

    grant_1 = GrantFactory(
        status=Grant.Status.confirmed,
        conference=conference,
    )

    other_conf_grant_1_voucher = ConferenceVoucherFactory(
        user=grant_1.user,
        conference=other_conference,
        voucher_type=type,
    )

    grant_2 = GrantFactory(
        status=Grant.Status.confirmed,
        conference=conference,
    )
    request = rf.get("/")
    request.user = admin_user

    create_grant_vouchers(
        None,
        request=request,
        queryset=Grant.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.for_conference(conference).count() == 2

    grant_1_voucher = (
        ConferenceVoucher.objects.for_conference(conference)
        .filter(user_id=grant_1.user_id)
        .get()
    )
    assert grant_1_voucher.voucher_type == ConferenceVoucher.VoucherType.GRANT
    assert grant_1_voucher.conference == conference

    other_conf_grant_1_voucher.refresh_from_db()
    assert other_conf_grant_1_voucher.voucher_type == type
    assert other_conf_grant_1_voucher.conference_id == other_conference.id

    grant_2_voucher = ConferenceVoucher.objects.filter(user_id=grant_2.user_id).get()
    assert grant_2_voucher.voucher_type == ConferenceVoucher.VoucherType.GRANT
    assert grant_2_voucher.conference == conference

    mock_messages.success.assert_called_once_with(
        request,
        "Vouchers created!",
    )


def test_create_grant_vouchers_co_speaker_voucher_is_upgraded(rf, mocker, admin_user):
    mock_messages = mocker.patch("grants.admin.messages")

    conference = ConferenceFactory()

    grant_1 = GrantFactory(
        status=Grant.Status.confirmed,
        conference=conference,
    )

    grant_1_voucher = ConferenceVoucherFactory(
        user=grant_1.user,
        conference=conference,
        voucher_type=ConferenceVoucher.VoucherType.CO_SPEAKER,
    )

    grant_2 = GrantFactory(
        status=Grant.Status.confirmed,
        conference=conference,
    )
    request = rf.get("/")
    request.user = admin_user

    create_grant_vouchers(
        None,
        request=request,
        queryset=Grant.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.for_conference(conference).count() == 2

    grant_1_voucher = ConferenceVoucher.objects.filter(user_id=grant_1.user_id).get()
    assert grant_1_voucher.voucher_type == ConferenceVoucher.VoucherType.GRANT
    assert grant_1_voucher.conference == conference

    grant_2_voucher = ConferenceVoucher.objects.filter(user_id=grant_2.user_id).get()
    assert grant_2_voucher.voucher_type == ConferenceVoucher.VoucherType.GRANT
    assert grant_2_voucher.conference == conference

    mock_messages.success.assert_called_once_with(
        request,
        "Vouchers created!",
    )


def test_create_grant_vouchers_only_for_confirmed_grants(rf, mocker, admin_user):
    mock_messages = mocker.patch("grants.admin.messages")
    conference = ConferenceFactory()
    grant_1 = GrantFactory(
        status=Grant.Status.refused,
        conference=conference,
    )
    grant_2 = GrantFactory(
        status=Grant.Status.confirmed,
        conference=conference,
    )
    request = rf.get("/")
    request.user = admin_user

    create_grant_vouchers(
        None,
        request=request,
        queryset=Grant.objects.filter(conference=conference),
    )

    assert ConferenceVoucher.objects.count() == 1
    assert not ConferenceVoucher.objects.filter(user_id=grant_1.user_id).exists()

    grant_2_voucher = ConferenceVoucher.objects.filter(user_id=grant_2.user_id).get()
    assert grant_2_voucher.voucher_type == ConferenceVoucher.VoucherType.GRANT

    mock_messages.error.assert_called_once_with(
        request,
        f"Grant for {grant_1.name} is not confirmed, we can't generate voucher for it.",
    )
    mock_messages.success.assert_called_once_with(
        request,
        "Vouchers created!",
    )


def test_mark_rejected_and_send_email(rf, mocker, admin_user):
    conference = ConferenceFactory()

    mock_messages = mocker.patch("grants.admin.messages")
    grant1 = GrantFactory(status=Grant.Status.waiting_list, conference=conference)
    grant2 = GrantFactory(status=Grant.Status.waiting_list_maybe, conference=conference)
    request = rf.get("/")
    request.user = admin_user
    mock_send_rejected_email = mocker.patch(
        "grants.admin.send_grant_reply_rejected_email.delay"
    )

    mark_rejected_and_send_email(None, request=request, queryset=Grant.objects.all())

    grant1.refresh_from_db()
    grant2.refresh_from_db()
    assert grant1.status == Grant.Status.rejected
    assert grant2.status == Grant.Status.rejected

    # Verify admin action was called correctly
    mock_messages.info.assert_has_calls(
        [
            call(request, f"Sent Rejected reply email to {grant1.name}"),
            call(request, f"Sent Rejected reply email to {grant2.name}"),
        ],
        any_order=True,
    )

    # Verify task was queued correctly
    mock_send_rejected_email.assert_has_calls(
        [call(grant_id=grant1.id), call(grant_id=grant2.id)], any_order=True
    )

    # Verify audit log entries were created correctly
    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant1.id,
        change_message="Status changed from 'waiting_list' to 'rejected' and rejection email sent",
    ).exists()
    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant2.id,
        change_message="Status changed from 'waiting_list_maybe' to 'rejected' and rejection email sent",
    ).exists()


def test_confirm_pending_status_action(rf, admin_user):
    grant_1 = GrantFactory(
        status=Grant.Status.pending,
        pending_status=Grant.Status.confirmed,
    )

    grant_2 = GrantFactory(
        status=Grant.Status.rejected,
        pending_status=Grant.Status.waiting_list,
        conference=grant_1.conference,
    )

    grant_3 = GrantFactory(
        status=Grant.Status.waiting_list,
        pending_status=Grant.Status.waiting_list_maybe,
        conference=grant_1.conference,
    )

    grant_4 = GrantFactory(
        status=Grant.Status.waiting_list_maybe,
        pending_status=Grant.Status.confirmed,
        conference=grant_1.conference,
    )

    request = rf.get("/")
    request.user = admin_user
    confirm_pending_status(
        None, request, Grant.objects.filter(id__in=[grant_1.id, grant_2.id, grant_3.id])
    )

    grant_1.refresh_from_db()
    grant_2.refresh_from_db()
    grant_3.refresh_from_db()
    grant_4.refresh_from_db()

    assert grant_1.status == Grant.Status.confirmed
    assert grant_2.status == Grant.Status.waiting_list
    assert grant_3.status == Grant.Status.waiting_list_maybe

    assert grant_1.pending_status is None
    assert grant_2.pending_status is None
    assert grant_3.pending_status is None

    # Verify audit log entries were created correctly
    assert LogEntry.objects.filter(
        object_id=grant_1.id,
        change_message="[Bulk Admin Action] Status changed from 'pending' to 'confirmed'.",
    ).exists()
    assert LogEntry.objects.filter(
        object_id=grant_2.id,
        change_message="[Bulk Admin Action] Status changed from 'rejected' to 'waiting_list'.",
    ).exists()
    assert LogEntry.objects.filter(
        object_id=grant_3.id,
        change_message="[Bulk Admin Action] Status changed from 'waiting_list' to 'waiting_list_maybe'.",
    ).exists()

    # Left out from the action
    assert grant_4.status == Grant.Status.waiting_list_maybe
    assert not LogEntry.objects.filter(
        object_id=grant_4.id,
    ).exists()


def test_reset_pending_status_back_to_status_action(rf, admin_user):
    grant_1 = GrantFactory(
        status=Grant.Status.pending,
        pending_status=Grant.Status.confirmed,
    )

    grant_2 = GrantFactory(
        status=Grant.Status.rejected,
        pending_status=Grant.Status.waiting_list,
        conference=grant_1.conference,
    )

    grant_3 = GrantFactory(
        status=Grant.Status.waiting_list,
        pending_status=Grant.Status.waiting_list_maybe,
        conference=grant_1.conference,
    )

    grant_4 = GrantFactory(
        status=Grant.Status.waiting_list_maybe,
        pending_status=Grant.Status.confirmed,
        conference=grant_1.conference,
    )

    request = rf.get("/")
    request.user = admin_user
    reset_pending_status_back_to_status(
        None, request, Grant.objects.filter(id__in=[grant_1.id, grant_2.id, grant_3.id])
    )

    grant_1.refresh_from_db()
    grant_2.refresh_from_db()
    grant_3.refresh_from_db()
    grant_4.refresh_from_db()

    assert grant_1.status == Grant.Status.pending
    assert grant_1.pending_status is None

    assert grant_2.status == Grant.Status.rejected
    assert grant_2.pending_status is None

    assert grant_3.status == Grant.Status.waiting_list
    assert grant_3.pending_status is None

    # Verify audit log entries were created correctly
    assert LogEntry.objects.filter(
        object_id=grant_1.id,
        change_message="[Bulk Admin Action] pending_status reset from 'confirmed' to None.",
    ).exists()
    assert LogEntry.objects.filter(
        object_id=grant_2.id,
        change_message="[Bulk Admin Action] pending_status reset from 'waiting_list' to None.",
    ).exists()
    assert LogEntry.objects.filter(
        object_id=grant_3.id,
        change_message="[Bulk Admin Action] pending_status reset from 'waiting_list_maybe' to None.",
    ).exists()

    # Left out from the action
    assert grant_4.status == Grant.Status.waiting_list_maybe
    assert grant_4.pending_status == Grant.Status.confirmed
    assert not LogEntry.objects.filter(
        object_id=grant_4.id,
    ).exists()


def test_delete_reimbursement_from_admin_logs_audit_log_entry(rf, admin_user):
    grant = GrantFactory()
    reimbursement = GrantReimbursementFactory(
        grant=grant,
        category__conference=grant.conference,
        category__ticket=True,
        granted_amount=Decimal("100"),
    )

    request = rf.get("/")
    request.user = admin_user

    admin = GrantReimbursementAdmin(GrantReimbursement, AdminSite())
    admin.delete_model(request, reimbursement)

    # Verify reimbursement was deleted
    assert not GrantReimbursement.objects.filter(id=reimbursement.id).exists()

    # Verify audit log entry was created correctly
    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant.id,
        change_message=f"Reimbursement removed: {reimbursement.category.name}",
    ).exists()


def test_save_grant_in_admin_logs_audit_log_entry(rf, admin_user):
    grant = GrantFactory()
    request = rf.get("/")
    request.user = admin_user

    admin = GrantAdmin(Grant, AdminSite())
    admin.save_model(request, grant, None, False)

    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant.id,
        change_message="Grant created",
    ).exists()


def test_save_grant_in_admin_logs_audit_log_entry_for_status_change(rf, admin_user):
    grant = GrantFactory(status=Grant.Status.pending)
    request = rf.get("/")
    request.user = admin_user

    admin = GrantAdmin(Grant, AdminSite())
    grant.status = Grant.Status.confirmed
    admin.save_model(request, grant, None, True)

    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant.id,
        change_message="Status changed from 'pending' to 'confirmed'",
    ).exists()


def test_save_grant_in_admin_logs_audit_log_entry_for_pending_status_change(
    rf, admin_user
):
    grant = GrantFactory(pending_status=Grant.Status.pending)
    request = rf.get("/")
    request.user = admin_user

    admin = GrantAdmin(Grant, AdminSite())
    grant.pending_status = Grant.Status.confirmed
    admin.save_model(request, grant, None, True)

    assert LogEntry.objects.filter(
        user=admin_user,
        object_id=grant.id,
        change_message="Pending status changed from 'pending' to 'confirmed'",
    ).exists()
