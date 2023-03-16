from collections import Counter
from datetime import timedelta
from itertools import groupby
from typing import Dict, List, Optional

from django import forms
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.utils import timezone
from import_export.admin import ExportMixin
from import_export.fields import Field

from countries import countries
from domain_events.publisher import (
    send_grant_reply_approved_email,
    send_grant_reply_rejected_email,
    send_grant_reply_waiting_list_email,
    send_grant_reply_waiting_list_update_email,
)
from schedule.models import ScheduleItem
from submissions.models import Submission
from users.autocomplete import UsersBackendAutocomplete
from users.mixins import AdminUsersMixin, ResourceUsersByIdsMixin, SearchUsersMixin

from .models import Grant, GrantRecap

EXPORT_GRANTS_FIELDS = (
    "name",
    "full_name",
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
    "traveling_from",
    "conference__code",
    "created",
)


class GrantResource(ResourceUsersByIdsMixin):
    search_field = "user_id"
    age_group = Field()
    has_sent_submission = Field()
    submission_title = Field()
    submission_tags = Field()
    submission_admin_link = Field()
    submission_pycon_link = Field()
    grant_admin_link = Field()
    USERS_SUBMISSIONS: Dict[int, List[Submission]] = {}

    def dehydrate_age_group(self, obj: Grant):
        return Grant.AgeGroup(obj.age_group).label

    def dehydrate_has_sent_submission(self, obj: Grant) -> str:
        return "TRUE" if obj.user_id in self.USERS_SUBMISSIONS else "FALSE"

    def _get_submissions(self, obj: Grant) -> Optional[List[Submission]]:
        if not obj.user_id:
            return

        return self.USERS_SUBMISSIONS.get(obj.user_id)

    def dehydrate_submission_title(self, obj: Grant):
        submissions = self._get_submissions(obj)
        if not submissions:
            return

        return "\n".join([s.title.localize("en") for s in submissions])

    def dehydrate_submission_tags(self, obj: Grant):
        submissions = self._get_submissions(obj)
        if not submissions:
            return

        return "\n".join(
            [
                ", ".join(
                    [
                        f"{r.tag.name}: {r.rank} / {r.total_submissions_per_tag}"
                        for r in s.rankings.all()
                    ]
                )
                for s in submissions
            ]
        )

    def dehydrate_submission_pycon_link(self, obj):
        submissions = self.USERS_SUBMISSIONS.get(obj.user_id)
        if not submissions:
            return
        return "\n".join(
            [f"https://pycon.it/submission/{s.hashid}" for s in submissions]
        )

    def dehydrate_submission_admin_link(self, obj):
        submissions = self.USERS_SUBMISSIONS.get(obj.user_id)
        if not submissions:
            return
        return "\n".join(
            [
                f"https://admin.pycon.it/admin/submissions/submission/{s.id}/change/"
                for s in submissions
            ]
        )

    def dehydrate_grant_admin_link(self, obj: Grant):
        return f"https://admin.pycon.it/admin/grants/grant/?q={'+'.join(obj.full_name.split(' '))}"  # noqa: E501

    def before_export(self, queryset: QuerySet, *args, **kwargs):
        super().before_export(queryset, *args, **kwargs)
        conference_id = queryset.values_list("conference_id").first()

        submissions = Submission.objects.prefetch_related(
            "rankings__tag", "rankings__submission"
        ).filter(
            speaker_id__in=self._PREFETCHED_USERS_BY_ID.keys(),
            conference_id=conference_id,
        )

        self.USERS_SUBMISSIONS = {}
        for submission in submissions:
            self.USERS_SUBMISSIONS.setdefault(submission.speaker_id, [])
            self.USERS_SUBMISSIONS[submission.speaker_id].append(submission)

        return queryset

    class Meta:
        model = Grant
        fields = EXPORT_GRANTS_FIELDS
        export_order = EXPORT_GRANTS_FIELDS


@admin.action(description="Send Approved/Waiting List/Rejected reply emails")
def send_reply_emails(modeladmin, request, queryset):
    queryset = queryset.filter(
        status__in=(
            Grant.Status.approved,
            Grant.Status.waiting_list,
            Grant.Status.waiting_list_maybe,
            Grant.Status.rejected,
        ),
    )

    if not queryset:
        messages.add_message(
            request, messages.WARNING, "No grants found in the selection"
        )
        return

    for grant in queryset:
        if grant.status in (Grant.Status.approved,):
            if grant.approved_type is None:
                messages.error(
                    request,
                    f"Grant for {grant.name} is missing 'Grant Approved Type'!",
                )
                return

            if grant.grant_type != Grant.ApprovedType.ticket_only and (
                grant.total_amount is None
                or grant.accommodation_amount is None
                or grant.total_amount is None
            ):
                messages.error(
                    request,
                    f"Grant for {grant.name} is missing 'Approved Amount'!",
                )
                return

            now = timezone.now()
            grant.applicant_reply_deadline = timezone.datetime(
                now.year, now.month, now.day, 23, 59, 59
            ) + timedelta(days=14)
            grant.save()
            send_grant_reply_approved_email(grant)

            messages.info(request, f"Sent Approved reply email to {grant.name}")

        if (
            grant.status == Grant.Status.waiting_list
            or grant.status == Grant.Status.waiting_list_maybe
        ):
            send_grant_reply_waiting_list_email(grant)
            messages.info(request, f"Sent Waiting List reply email to {grant.name}")

        if grant.status == Grant.Status.rejected:
            send_grant_reply_rejected_email(grant)
            messages.info(request, f"Sent Rejected reply email to {grant.name}")


@admin.action(description="Send reminder to waiting confirmation grants")
def send_grant_reminder_to_waiting_for_confirmation(modeladmin, request, queryset):
    queryset = queryset.filter(
        status__in=(Grant.Status.waiting_for_confirmation,),
    )

    for grant in queryset:
        if not grant.grant_type:
            messages.add_message(
                request,
                messages.ERROR,
                f"Grant for {grant.name} is missing 'Grant Approved Type'!",
            )
            return

        if grant.grant_type != Grant.ApprovedType.ticket_only and (
            grant.total_amount is None
            or grant.accommodation_amount is None
            or grant.total_amount is None
        ):
            messages.add_message(
                request,
                messages.ERROR,
                f"Grant for {grant.name} is missing 'Grant Approved Amount'!",
            )
            return

        send_grant_reply_approved_email(grant, is_reminder=True)

        messages.info(request, f"Grant reminder sent to {grant.name}")


@admin.action(description="Send Waiting List update email")
def send_reply_email_waiting_list_update(modeladmin, request, queryset):
    queryset = queryset.filter(
        status__in=(
            Grant.Status.waiting_list,
            Grant.Status.waiting_list_maybe,
        ),
    )

    for grant in queryset:
        send_grant_reply_waiting_list_update_email(grant)
        messages.info(request, f"Sent Waiting List update reply email to {grant.name}")


class GrantAdminForm(forms.ModelForm):
    class Meta:
        model = Grant
        widgets = {
            "user_id": UsersBackendAutocomplete(admin.site),
        }
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
            "user_id",
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
            "traveling_from",
            "country_type",
            "applicant_message",
            "applicant_reply_sent_at",
            "applicant_reply_deadline",
        )


@admin.register(Grant)
class GrantAdmin(ExportMixin, AdminUsersMixin, SearchUsersMixin):
    speaker_ids = []
    resource_class = GrantResource
    form = GrantAdminForm
    list_display = (
        "user_display_name",
        "country",
        "is_speaker",
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
    )
    list_filter = (
        "conference",
        "status",
        "country_type",
        "occupation",
        "grant_type",
        "interested_in_volunteering",
        "traveling_from",
    )
    search_fields = (
        "email",
        "full_name",
        "travelling_from",
        "been_to_other_events",
        "why",
        "notes",
    )
    user_fk = "user_id"
    actions = [
        send_reply_emails,
        send_grant_reminder_to_waiting_for_confirmation,
        send_reply_email_waiting_list_update,
        "delete_selected",
    ]

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
                    "applicant_reply_sent_at",
                    "applicant_reply_deadline",
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
                    "user_id",
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
                    "travelling_from",
                    "traveling_from",
                    "why",
                    "python_usage",
                    "been_to_other_events",
                    "interested_in_volunteering",
                    "notes",
                )
            },
        ),
    )

    @admin.display(
        description="User",
    )
    def user_display_name(self, obj):
        if obj.user_id:
            return self.get_user_display_name(obj.user_id)
        return obj.email

    @admin.display(
        description="C",
    )
    def country(self, obj):
        if obj.traveling_from:
            country = countries.get(code=obj.traveling_from)
            if country:
                return country.emoji

        return ""

    @admin.display(
        description="S",
    )
    def is_speaker(self, obj):
        if obj.user_id in self.speaker_ids:
            return "🗣️"
        return ""

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        if not self.speaker_ids:
            conference_id = qs.values_list("conference_id").first()
            self.speaker_ids = ScheduleItem.objects.filter(
                conference__id__in=conference_id,
                submission__speaker_id__isnull=False,
            ).values_list("submission__speaker_id", flat=True)
        return qs

    def save_form(self, request, form, change):
        # If the status, country_type or approved_type changes and the grant is approved
        # we need to recalculate the totals
        if form.cleaned_data["status"] == Grant.Status.approved and (
            form.cleaned_data["status"] != form.initial.get("status")
            or form.cleaned_data["country_type"] != form.initial.get("country_type")
            or form.cleaned_data["approved_type"] != form.initial.get("approved_type")
        ):
            conference = form.cleaned_data["conference"]
            form.instance.ticket_amount = conference.grants_default_ticket_amount

            if form.cleaned_data["approved_type"] not in (
                Grant.ApprovedType.ticket_only,
                Grant.ApprovedType.ticket_travel,
            ):
                form.instance.accommodation_amount = (
                    conference.grants_default_accommodation_amount
                )

            if form.cleaned_data["country_type"] == Grant.CountryType.italy:
                form.instance.travel_amount = (
                    conference.grants_default_travel_from_italy_amount
                )
            elif form.cleaned_data["country_type"] == Grant.CountryType.europe:
                form.instance.travel_amount = (
                    conference.grants_default_travel_from_europe_amount
                )
            elif form.cleaned_data["country_type"] == Grant.CountryType.extra_eu:
                form.instance.travel_amount = (
                    conference.grants_default_travel_from_extra_eu_amount
                )

            form.instance.total_amount = (
                form.instance.ticket_amount
                + form.instance.accommodation_amount
                + form.instance.travel_amount
            )

        return_value = super().save_form(request, form, change)

        return return_value

    class Media:
        js = ["admin/js/jquery.init.js"]


@admin.register(GrantRecap)
class GrantsRecap(admin.ModelAdmin):
    list_filter = ("conference",)
    qs = None

    def has_change_permission(self, *args, **kwargs) -> bool:
        return False

    def get_queryset(self, request):
        if self.qs:
            return self.qs

        self.qs = super().get_queryset(request)
        filters = dict(request.GET.items())

        if filters:
            self.qs = self.qs.filter(**filters)

        return self.qs

    def changelist_view(self, request, extra_context=None):
        qs = self.get_queryset(request).order_by("traveling_from")

        results = []
        for country_code, group in groupby(list(qs), key=lambda k: k.traveling_from):
            country = countries.get(code=country_code)
            if not country:
                continue
            grants = list(group)
            counter = Counter([g.status for g in grants])
            results.append(
                {
                    "continent": country.continent.name,
                    "country": country.name,
                    "total": int(sum([g.total_amount for g in grants])),
                    "count": len(grants),
                    "rejected": counter.get(Grant.Status.rejected, 0),
                    "approved": counter.get(Grant.Status.approved, 0),
                    "waiting_list": counter.get(Grant.Status.waiting_list, 0)
                    + counter.get(Grant.Status.waiting_list_maybe, 0),
                    "waiting_for_confirmation": counter.get(
                        Grant.Status.waiting_for_confirmation, 0
                    ),
                    "refused": counter.get(Grant.Status.refused, 0),
                    "confirmed": counter.get(Grant.Status.confirmed, 0),
                }
            )

        results = sorted(results, key=lambda k: (-k["count"], k["continent"]))

        counter = Counter([g.status for g in qs])
        footer = {
            "title": "Total",
            "count": len(qs),
            "total": int(
                sum(
                    [
                        g.total_amount
                        for g in qs
                        if g.status
                        in (
                            Grant.Status.confirmed,
                            Grant.Status.approved,
                            Grant.Status.waiting_for_confirmation,
                        )
                    ]
                )
            ),
            "rejected": counter.get(Grant.Status.rejected, 0),
            "approved": counter.get(Grant.Status.approved, 0),
            "waiting_list": counter.get(Grant.Status.waiting_list, 0)
            + counter.get(Grant.Status.waiting_list_maybe, 0),
            "waiting_for_confirmation": counter.get(
                Grant.Status.waiting_for_confirmation, 0
            ),
            "refused": counter.get(Grant.Status.refused, 0),
            "confirmed": counter.get(Grant.Status.confirmed, 0),
        }

        extra_context = {"results": results, "footer": footer}
        return super().changelist_view(request, extra_context=extra_context)
