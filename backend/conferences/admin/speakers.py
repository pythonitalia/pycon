from django.contrib import admin
from conferences.models import SpeakerVoucher
from .actions import create_speaker_vouchers_on_pretix, send_voucher_via_email
from .forms import SpeakerVoucherForm


@admin.register(SpeakerVoucher)
class SpeakerVoucherAdmin(admin.ModelAdmin):
    form = SpeakerVoucherForm
    search_fields = ("voucher_code", "user__name", "user__full_name")
    autocomplete_fields = ("user",)
    list_filter = (
        "conference",
        "voucher_type",
        ("pretix_voucher_id", admin.EmptyFieldListFilter),
    )
    list_display = (
        "conference",
        "user_display_name",
        "voucher_type",
        "voucher_code",
        "created_on_pretix",
        "voucher_email_sent_at",
        "created",
    )
    actions = [
        create_speaker_vouchers_on_pretix,
        send_voucher_via_email,
    ]

    @admin.display(
        boolean=True,
    )
    def created_on_pretix(self, obj):
        return obj.pretix_voucher_id is not None

    def get_changeform_initial_data(self, request):
        return {"voucher_code": SpeakerVoucher.generate_code()}

    def user_display_name(self, obj):
        return obj.user.display_name
