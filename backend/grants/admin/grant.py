from countries.filters import CountryFilter
from django import forms
from django.contrib import admin
from users.admin_mixins import ConferencePermissionMixin
from countries import countries
from schedule.models import ScheduleItem
from submissions.models import Submission
from grants.models import Grant
from django.db.models import Exists, OuterRef


from grants.admin.filters import IsProposedSpeakerFilter, IsConfirmedSpeakerFilter

from grants.admin.actions import (
    send_reply_emails,
    send_grant_reminder_to_waiting_for_confirmation,
    send_reply_email_waiting_list_update,
    create_grant_vouchers_on_pretix,
    send_voucher_via_email,
)


class GrantAdminForm(forms.ModelForm):
    class Meta:
        model = Grant
        fields = (
            "id",
            "name",
            "status",
            "approved_type",
            "ticket_amount",
            "travel_amount",
            "accommodation_amount",
            "total_amount",
            "full_name",
            "conference",
            "user",
            "age_group",
            "gender",
            "occupation",
            "grant_type",
            "python_usage",
            "been_to_other_events",
            "interested_in_volunteering",
            "needs_funds_for_travel",
            "why",
            "notes",
            "travelling_from",
            "country_type",
            "applicant_message",
            "plain_thread_id",
            "applicant_reply_sent_at",
            "applicant_reply_deadline",
        )


@admin.register(Grant)
class GrantAdmin(ConferencePermissionMixin, admin.ModelAdmin):
    change_list_template = "admin/grants/grant/change_list.html"
    form = GrantAdminForm
    list_display = (
        "user_display_name",
        "country",
        "is_proposed_speaker",
        "is_confirmed_speaker",
        "conference",
        "status",
        "approved_type",
        "ticket_amount",
        "travel_amount",
        "accommodation_amount",
        "total_amount",
        "country_type",
        "applicant_reply_sent_at",
        "applicant_reply_deadline",
        "voucher_code",
        "voucher_email_sent_at",
        "created",
    )
    readonly_fields = (
        "applicant_message",
        "plain_thread_id",
    )
    list_filter = (
        "conference",
        "status",
        "country_type",
        "occupation",
        "grant_type",
        "interested_in_volunteering",
        IsProposedSpeakerFilter,
        IsConfirmedSpeakerFilter,
        ("travelling_from", CountryFilter),
    )
    search_fields = (
        "email",
        "full_name",
        "travelling_from",
        "been_to_other_events",
        "why",
        "notes",
    )
    actions = [
        send_reply_emails,
        send_grant_reminder_to_waiting_for_confirmation,
        send_reply_email_waiting_list_update,
        create_grant_vouchers_on_pretix,
        send_voucher_via_email,
        "delete_selected",
    ]
    autocomplete_fields = ("user",)

    fieldsets = (
        (
            "Manage the Grant",
            {
                "fields": (
                    "status",
                    "approved_type",
                    "country_type",
                    "ticket_amount",
                    "travel_amount",
                    "accommodation_amount",
                    "total_amount",
                    "applicant_message",
                    "plain_thread_id",
                    "applicant_reply_sent_at",
                    "applicant_reply_deadline",
                    "pretix_voucher_id",
                    "voucher_code",
                    "voucher_email_sent_at",
                )
            },
        ),
        (
            "About the Applicant",
            {
                "fields": (
                    "name",
                    "full_name",
                    "conference",
                    "user",
                    "age_group",
                    "gender",
                    "occupation",
                )
            },
        ),
        (
            "The Grant",
            {
                "fields": (
                    "grant_type",
                    "needs_funds_for_travel",
                    "need_visa",
                    "need_accommodation",
                    "travelling_from",
                    "why",
                    "python_usage",
                    "been_to_other_events",
                    "community_contribution",
                    "interested_in_volunteering",
                    "notes",
                    "website",
                    "twitter_handle",
                    "github_handle",
                    "linkedin_url",
                    "mastodon_handle",
                )
            },
        ),
    )

    @admin.display(
        description="User",
    )
    def user_display_name(self, obj):
        if obj.user_id:
            return obj.user.display_name
        return obj.email

    @admin.display(
        description="C",
    )
    def country(self, obj):
        if obj.travelling_from:
            country = countries.get(code=obj.travelling_from)
            if country:
                return country.emoji

        return ""

    @admin.display(description="✍️")
    def is_proposed_speaker(self, obj):
        if obj.is_proposed_speaker:
            return "✍️"
        return ""

    @admin.display(description="🗣️")
    def is_confirmed_speaker(self, obj):
        if obj.is_confirmed_speaker:
            return "🗣️"
        return ""

    def get_queryset(self, request):
        qs = (
            super()
            .get_queryset(request)
            .annotate(
                is_proposed_speaker=Exists(
                    Submission.objects.non_cancelled().filter(
                        conference_id=OuterRef("conference_id"),
                        speaker_id=OuterRef("user_id"),
                    )
                ),
                is_confirmed_speaker=Exists(
                    ScheduleItem.objects.filter(
                        conference_id=OuterRef("conference_id"),
                        submission__speaker_id=OuterRef("user_id"),
                    )
                ),
            )
        )
        return qs

    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path(
    #             "summary/",
    #             self.admin_site.admin_view(self.summary_view),
    #             name="grants-summary",
    #         ),
    #     ]
    #     return custom_urls + urls

    class Media:
        js = ["admin/js/jquery.init.js"]
