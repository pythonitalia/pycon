from countries.filters import CountryFilter
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Count, Sum
from helpers.constants import GENDERS
from django import forms
from django.contrib import admin
from users.admin_mixins import ConferencePermissionMixin
from countries import countries
from schedule.models import ScheduleItem
from submissions.models import Submission
from .models import Grant
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "summary/",
                self.admin_site.admin_view(self.summary_view),
                name="grants-summary",
            ),
        ]
        return custom_urls + urls

    def summary_view(self, request):
        """
        Custom view for summarizing Grant data in the Django admin.
        Aggregates data by country and status, and applies request filters.
        """
        statuses = Grant.Status.choices

        filtered_grants, formatted_filters = self._filter_and_format_grants(request)

        grants_by_country = filtered_grants.values(
            "travelling_from", "status"
        ).annotate(total=Count("id"))

        (
            country_stats,
            status_totals,
            totals_per_continent,
        ) = self._aggregate_data_by_country(grants_by_country, statuses)
        gender_stats = self._aggregate_data_by_gender(filtered_grants, statuses)
        financial_summary, total_amount = self._aggregate_financial_data_by_status(
            filtered_grants, statuses
        )

        sorted_country_stats = dict(
            sorted(country_stats.items(), key=lambda x: (x[0][0], x[0][2]))
        )

        context = {
            "country_stats": sorted_country_stats,
            "statuses": statuses,
            "genders": {code: name for code, name in GENDERS},
            "financial_summary": financial_summary,
            "total_amount": total_amount,
            "total_grants": filtered_grants.count(),
            "status_totals": status_totals,
            "totals_per_continent": totals_per_continent,
            "gender_stats": gender_stats,
            "filters": formatted_filters,
            **self.admin_site.each_context(request),
        }
        return TemplateResponse(request, "admin/grants/grant_summary.html", context)

    def _aggregate_data_by_country(self, grants_by_country, statuses):
        """
        Aggregates grant data by country and status.
        """

        summary = {}
        status_totals = {status[0]: 0 for status in statuses}
        totals_per_continent = {}

        for data in grants_by_country:
            country = countries.get(code=data["travelling_from"])
            continent = country.continent.name if country else "Unknown"
            country_name = f"{country.name} {country.emoji}" if country else "Unknown"
            country_code = country.code if country else "Unknown"
            key = (continent, country_name, country_code)

            if key not in summary:
                summary[key] = {status[0]: 0 for status in statuses}

            summary[key][data["status"]] += data["total"]
            status_totals[data["status"]] += data["total"]

            # Update continent totals
            if continent not in totals_per_continent:
                totals_per_continent[continent] = {status[0]: 0 for status in statuses}
            totals_per_continent[continent][data["status"]] += data["total"]

        return summary, status_totals, totals_per_continent

    def _aggregate_data_by_gender(self, filtered_grants, statuses):
        """
        Aggregates grant data by gender and status.
        """
        gender_data = filtered_grants.values("gender", "status").annotate(
            total=Count("id")
        )
        gender_summary = {
            gender: {status[0]: 0 for status in statuses} for gender, _ in GENDERS
        }
        gender_summary[""] = {
            status[0]: 0 for status in statuses
        }  # For unspecified genders

        for data in gender_data:
            gender = data["gender"] if data["gender"] else ""
            status = data["status"]
            total = data["total"]
            gender_summary[gender][status] += total

        return gender_summary

    def _aggregate_financial_data_by_status(self, filtered_grants, statuses):
        """
        Aggregates financial data (total amounts) by grant status.
        """
        financial_data = filtered_grants.values("status").annotate(
            total_amount_sum=Sum("total_amount")
        )
        financial_summary = {status[0]: 0 for status in statuses}
        overall_total = 0

        for data in financial_data:
            status = data["status"]
            total_amount = data["total_amount_sum"] or 0
            financial_summary[status] += total_amount
            overall_total += total_amount

        return financial_summary, overall_total

    def _filter_and_format_grants(self, request):
        """
        Filters the Grant queryset based on request parameters and
        formats the filter keys for display.
        """
        field_lookups = [
            "__exact",
            "__in",
            "__gt",
            "__lt",
            "__contains",
            "__startswith",
            "__endswith",
            "__range",
            "__isnull",
        ]

        filter_mapping = {
            "conference__id": "Conference ID",
            "status": "Status",
            "country_type": "Country Type",
            "occupation": "Occupation",
            "grant_type": "Grant Type",
            "travelling_from": "Country",
        }

        # Construct a set of allowed filters
        allowed_filters = {
            f + lookup for f in filter_mapping.keys() for lookup in field_lookups
        }

        def map_filter_key(key):
            """Helper function to map raw filter keys to user-friendly names"""
            base_key = next(
                (
                    key[: -len(lookup)]
                    for lookup in field_lookups
                    if key.endswith(lookup)
                ),
                key,
            )
            return filter_mapping.get(base_key, base_key.capitalize())

        # Apply filtered parameters and format filter keys for display
        raw_filter_params = {
            k: v for k, v in request.GET.items() if k in allowed_filters
        }
        filter_params = {map_filter_key(k): v for k, v in raw_filter_params.items()}

        filtered_grants = Grant.objects.filter(**raw_filter_params)

        return filtered_grants, filter_params

    class Media:
        js = ["admin/js/jquery.init.js"]
