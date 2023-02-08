from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from participants.models import Participant
from users.autocomplete import UsersBackendAutocomplete
from users.mixins import AdminUsersMixin, SearchUsersMixin


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        widgets = {
            "user_id": UsersBackendAutocomplete(admin.site),
        }
        fields = [
            "conference",
            "user_id",
            "photo",
            "bio",
            "website",
            "twitter_handle",
            "instagram_handle",
            "linkedin_url",
            "facebook_url",
            "mastodon_handle",
            "speaker_level",
            "previous_talk_video",
        ]


@admin.register(Participant)
class ParticipantAdmin(AdminUsersMixin, SearchUsersMixin):
    user_fk = "user_id"
    form = ParticipantForm
    list_display = (
        "user_display_name",
        "conference",
    )
    list_filter = ("conference",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "conference",
                    "user_id",
                    "photo",
                    "photo_preview",
                    "bio",
                    "website",
                    "twitter_handle",
                    "instagram_handle",
                    "linkedin_url",
                    "facebook_url",
                    "mastodon_handle",
                    "speaker_level",
                    "previous_talk_video",
                ),
            },
        ),
    )
    readonly_fields = (
        "photo_preview",
        "user_display_name",
    )

    def user_display_name(self, obj):
        if obj:
            return self.get_user_display_name(obj.user_id)

    def photo_preview(self, obj):
        if obj:
            return mark_safe(f'<img src="{obj.photo}" width="200" />')
