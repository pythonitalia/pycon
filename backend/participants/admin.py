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
