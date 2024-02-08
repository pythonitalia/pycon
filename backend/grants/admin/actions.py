from datetime import timedelta
from django.contrib import admin, messages
from django.utils import timezone
from django.utils.crypto import get_random_string
from grants.tasks import (
    send_grant_reply_approved_email,
    send_grant_reply_waiting_list_email,
    send_grant_reply_waiting_list_update_email,
    send_grant_reply_rejected_email,
    send_grant_voucher_email,
)
from pretix import create_voucher
from grants.models import Grant

from functools import wraps


def _check_amounts_are_not_empty(grant: Grant, request):
    if grant.total_amount is None:
        messages.error(
            request,
            f"Grant for {grant.name} is missing 'Total Amount'!",
        )
        return False

    if grant.has_approved_accommodation() and grant.accommodation_amount is None:
        messages.error(
            request,
            f"Grant for {grant.name} is missing 'Accommodation Amount'!",
        )
        return False

    if grant.has_approved_travel() and grant.travel_amount is None:
        messages.error(
            request,
            f"Grant for {grant.name} is missing 'Travel Amount'!",
        )
        return False

    return True


def validate_single_conference_selection(func):
    """
    Ensure all selected grants in the queryset belong to the same conference.
    """

    @wraps(func)
    def wrapper(modeladmin, request, queryset):
        is_filtered_by_conference = (
            queryset.values_list("conference_id").distinct().count() == 1
        )

        if not is_filtered_by_conference:
            messages.error(request, "Please select only one conference")
            return

        return func(modeladmin, request, queryset)

    return wrapper


@admin.action(description="Send Approved/Waiting List/Rejected reply emails")
@validate_single_conference_selection
def send_reply_emails(modeladmin, request, queryset):
    conference = queryset.first().conference

    if not conference.visa_application_form_link:
        messages.error(
            request,
            "Visa Application Form Link Missing: Please ensure the link to the Visa "
            "Application Form is set in the Conference admin settings.",
        )
        return

    queryset = queryset.filter(
        status__in=(
            Grant.Status.approved,
            Grant.Status.waiting_list,
            Grant.Status.waiting_list_maybe,
            Grant.Status.rejected,
        ),
    )

    if not queryset:
        messages.add_message(
            request, messages.WARNING, "No grants found in the selection"
        )
        return

    for grant in queryset:

        if grant.status in (Grant.Status.approved,):
            if grant.approved_type is None:
                messages.error(
                    request,
                    f"Grant for {grant.name} is missing 'Grant Approved Type'!",
                )
                return

            if not _check_amounts_are_not_empty(grant, request):
                return

            now = timezone.now()
            grant.applicant_reply_deadline = timezone.datetime(
                now.year, now.month, now.day, 23, 59, 59
            ) + timedelta(days=14)
            grant.save()
            send_grant_reply_approved_email.delay(grant_id=grant.id, is_reminder=False)

            messages.info(request, f"Sent Approved reply email to {grant.name}")

        if (
            grant.status == Grant.Status.waiting_list
            or grant.status == Grant.Status.waiting_list_maybe
        ):
            send_grant_reply_waiting_list_email.delay(grant_id=grant.id)
            messages.info(request, f"Sent Waiting List reply email to {grant.name}")

        if grant.status == Grant.Status.rejected:
            send_grant_reply_rejected_email.delay(grant_id=grant.id)
            messages.info(request, f"Sent Rejected reply email to {grant.name}")


@admin.action(description="Send reminder to waiting confirmation grants")
@validate_single_conference_selection
def send_grant_reminder_to_waiting_for_confirmation(modeladmin, request, queryset):
    queryset = queryset.filter(
        status__in=(Grant.Status.waiting_for_confirmation,),
    )

    for grant in queryset:
        if not grant.grant_type:
            messages.add_message(
                request,
                messages.ERROR,
                f"Grant for {grant.name} is missing 'Grant Approved Type'!",
            )
            return

        _check_amounts_are_not_empty(grant, request)

        send_grant_reply_approved_email.delay(grant_id=grant.id, is_reminder=True)

        messages.info(request, f"Grant reminder sent to {grant.name}")


@admin.action(description="Send Waiting List update email")
@validate_single_conference_selection
def send_reply_email_waiting_list_update(modeladmin, request, queryset):
    queryset = queryset.filter(
        status__in=(
            Grant.Status.waiting_list,
            Grant.Status.waiting_list_maybe,
        ),
    )

    for grant in queryset:
        send_grant_reply_waiting_list_update_email.delay(grant_id=grant.id)
        messages.info(request, f"Sent Waiting List update reply email to {grant.name}")


@admin.action(description="Send voucher via email")
@validate_single_conference_selection
def send_voucher_via_email(modeladmin, request, queryset):
    count = 0
    for grant in queryset.filter(pretix_voucher_id__isnull=False):
        send_grant_voucher_email.delay(grant_id=grant.id)
        count = count + 1

    messages.success(request, f"{count} Voucher emails scheduled!")


def _generate_voucher_code(prefix: str) -> str:
    charset = list("ABCDEFGHKLMNPQRSTUVWXYZ23456789")
    random_string = get_random_string(length=20, allowed_chars=charset)
    return f"{prefix}-{random_string}"


@admin.action(description="Create grant vouchers on Pretix")
@validate_single_conference_selection
def create_grant_vouchers_on_pretix(modeladmin, request, queryset):
    conference = queryset.first().conference

    if not conference.pretix_speaker_voucher_quota_id:
        messages.error(
            request,
            "Please configure the grant voucher quota ID in the conference settings",
        )
        return

    count = 0
    for grant in queryset.filter(pretix_voucher_id__isnull=True):
        if grant.status != Grant.Status.confirmed:
            messages.error(
                request,
                f"Grant for {grant.name} is not confirmed, "
                "we can't generate voucher for it.",
            )
            continue

        voucher_code = _generate_voucher_code("GRANT")
        pretix_voucher = create_voucher(
            conference=grant.conference,
            code=voucher_code,
            comment=f"Voucher for user_id={grant.user_id}",
            tag="grants",
            quota_id=grant.conference.pretix_speaker_voucher_quota_id,
            price_mode="set",
            value="0.00",
        )

        pretix_voucher_id = pretix_voucher["id"]
        grant.pretix_voucher_id = pretix_voucher_id
        grant.voucher_code = voucher_code
        grant.save()
        count += 1

    messages.success(request, f"{count} Vouchers created on Pretix!")
