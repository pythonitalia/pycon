from django.contrib import admin, messages
from conferences.models import SpeakerVoucher
from pretix import create_voucher
from schedule.tasks import send_speaker_voucher_email


@admin.action(description="Send voucher via email")
def send_voucher_via_email(modeladmin, request, queryset):
    is_filtered_by_conference = (
        queryset.values_list("conference_id").distinct().count() == 1
    )

    if not is_filtered_by_conference:
        messages.error(request, "Please select only one conference")
        return

    count = 0
    for speaker_voucher in queryset.filter(pretix_voucher_id__isnull=False):
        send_speaker_voucher_email.delay(speaker_voucher_id=speaker_voucher.id)
        count = count + 1

    messages.success(request, f"{count} Voucher emails scheduled!")


@admin.action(description="Create speaker vouchers on Pretix")
def create_speaker_vouchers_on_pretix(modeladmin, request, queryset):
    is_filtered_by_conference = (
        queryset.values_list("conference_id").distinct().count() == 1
    )

    if not is_filtered_by_conference:
        messages.error(request, "Please select only one conference")
        return

    conference = queryset.only("conference_id").first().conference

    if not conference.pretix_speaker_voucher_quota_id:
        messages.error(
            request,
            "Please configure the speaker voucher quota ID in the conference settings",
        )
        return

    count = 0

    for speaker_voucher in queryset.filter(pretix_voucher_id__isnull=True):
        if speaker_voucher.voucher_type == SpeakerVoucher.VoucherType.SPEAKER:
            price_mode = "set"
            value = "0.00"
        elif speaker_voucher.voucher_type == SpeakerVoucher.VoucherType.CO_SPEAKER:
            price_mode = "percent"
            value = "25.00"

        pretix_voucher = create_voucher(
            conference=speaker_voucher.conference,
            code=speaker_voucher.voucher_code,
            comment=f"Voucher for user_id={speaker_voucher.user_id}",
            tag="speakers",
            quota_id=speaker_voucher.conference.pretix_speaker_voucher_quota_id,
            price_mode=price_mode,
            value=value,
        )

        pretix_voucher_id = pretix_voucher["id"]
        speaker_voucher.pretix_voucher_id = pretix_voucher_id
        speaker_voucher.save()
        count = count + 1

    messages.success(request, f"{count} Vouchers created on Pretix!")
