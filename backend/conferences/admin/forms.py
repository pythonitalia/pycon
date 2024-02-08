from django.forms.models import ModelForm
from conferences.models import (
    Deadline,
)
from conferences.models import KeynoteSpeaker, SpeakerVoucher


class DeadlineForm(ModelForm):
    class Meta:
        model = Deadline
        fields = ["start", "end", "name", "description", "type", "conference"]


class KeynoteSpeakerForm(ModelForm):
    class Meta:
        model = KeynoteSpeaker
        fields = (
            "keynote",
            "user",
        )


class SpeakerVoucherForm(ModelForm):
    class Meta:
        model = SpeakerVoucher
        fields = [
            "conference",
            "user",
            "voucher_type",
            "voucher_code",
            "pretix_voucher_id",
            "voucher_email_sent_at",
        ]
