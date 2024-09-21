from django.contrib import admin, messages
from custom_admin.admin import validate_single_conference_selection
from pretix import create_voucher
from schedule.tasks import send_speaker_voucher_email


@admin.action(description="Send voucher via email")
@validate_single_conference_selection
def send_voucher_via_email(modeladmin, request, queryset):
    count = 0
    for conference_voucher in queryset.filter(pretix_voucher_id__isnull=False):
        send_speaker_voucher_email.delay(speaker_voucher_id=conference_voucher.id)
        count = count + 1

    messages.success(request, f"{count} Voucher emails scheduled!")


@admin.action(description="Create vouchers on Pretix")
@validate_single_conference_selection
def create_conference_vouchers_on_pretix(modeladmin, request, queryset):
    conference = queryset.only("conference_id").first().conference

    if not conference.pretix_conference_voucher_quota_id:
        messages.error(
            request,
            "Please configure the conference voucher quota ID in the conference settings",
        )
        return

    count = 0

    for conference_voucher in queryset.filter(pretix_voucher_id__isnull=True):
        price_mode, value = conference_voucher.get_voucher_configuration()

        pretix_voucher = create_voucher(
            conference=conference_voucher.conference,
            code=conference_voucher.voucher_code,
            comment=f"Voucher for user_id={conference_voucher.user_id}",
            tag=conference_voucher.voucher_type,
            quota_id=conference_voucher.conference.pretix_conference_voucher_quota_id,
            price_mode=price_mode,
            value=value,
        )

        pretix_voucher_id = pretix_voucher["id"]
        conference_voucher.pretix_voucher_id = pretix_voucher_id
        conference_voucher.save()
        count = count + 1

    messages.success(request, f"{count} Vouchers created on Pretix!")
