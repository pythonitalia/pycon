from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from participants.models import Participant


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            "conference",
            "user",
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
class ParticipantAdmin(admin.ModelAdmin):
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
                    "user",
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
            return obj.user.display_name

    def photo_preview(self, obj):
        if obj:
            return mark_safe(f'<img src="{obj.photo}" width="200" />')
