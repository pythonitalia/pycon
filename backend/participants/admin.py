from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from custom_admin.admin import (
    HTTPS_URL_FORMFIELD_OVERRIDES,
    formfield_with_https_urls,
)
from participants.models import Participant


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        formfield_callback = formfield_with_https_urls
        fields = "__all__"


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    formfield_overrides = HTTPS_URL_FORMFIELD_OVERRIDES
    form = ParticipantForm
    search_fields = ("user__email", "user__full_name")
    list_display = (
        "id",
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
                    "photo_file",
                    "photo_file_preview",
                    "bio",
                    "website",
                    "twitter_handle",
                    "instagram_handle",
                    "linkedin_url",
                    "facebook_url",
                    "mastodon_handle",
                    "speaker_level",
                    "previous_talk_video",
                    "speaker_availabilities",
                ),
            },
        ),
    )
    readonly_fields = (
        "photo_preview",
        "photo_file_preview",
        "user_display_name",
    )
    autocomplete_fields = ("user", "photo_file")

    def user_display_name(self, obj):
        if obj:
            return obj.user.display_name

    def photo_preview(self, obj):
        if obj:
            return mark_safe(f'<img src="{obj.photo}" width="200" />')

    def photo_file_preview(self, obj):
        if not obj or not obj.photo_file_id:
            return

        return mark_safe(f'<img src="{obj.photo_file.url}" width="200" />')
