from django import forms
from django.contrib import admin

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
