from datetime import timedelta
from typing import Dict, List, Optional

from django import forms
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.utils import timezone
from import_export.admin import ExportMixin
from import_export.fields import Field

from domain_events.publisher import (
    send_grant_reply_approved_email,
    send_grant_reply_rejected_email,
    send_grant_reply_waiting_list_email,
)
from submissions.models import Submission
from users.autocomplete import UsersBackendAutocomplete
from users.mixins import AdminUsersMixin, ResourceUsersByIdsMixin, SearchUsersMixin

from .models import Grant

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
        return f"https://admin.pycon.it/admin/grants/grant/?q={'+'.join(obj.full_name.split(' '))}"

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

            if (
                grant.grant_type != Grant.ApprovedType.ticket_only
                and grant.approved_amount is None
            ):
                messages.error(
                    request,
                    f"Grant for {grant.name} is missing 'Approved Amount'!",
                )
                return

            grant.applicant_reply_deadline = timezone.now().date() + timedelta(days=14)
            grant.save()
            send_grant_reply_approved_email(grant)

            messages.info(request, f"Sent Approved reply email to {grant.name}")

        if (
            grant.status == Grant.Status.waiting_list
            or grant.status == Grant.Status.waiting_list_maybe
        ):
            if grant.applicant_reply_sent_at is not None:
                messages.warning(
                    request,
                    f"Reply email for {grant.name} was already sent! Skipping.",
                )
                return

            send_grant_reply_waiting_list_email(grant)
            messages.info(request, f"Sent Waiting List reply email to {grant.name}")

        if grant.status == Grant.Status.rejected:
            if grant.applicant_reply_sent_at is not None:
                messages.warning(
                    request,
                    f"Reply email for {grant.name} was already sent! Skipping.",
                )
                return

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

        if (
            grant.grant_type != Grant.ApprovedType.ticket_only
            and grant.approved_amount is None
        ):
            messages.add_message(
                request,
                messages.ERROR,
                f"Grant for {grant.name} is missing 'Grant Approved Amount'!",
            )
            return

        send_grant_reply_approved_email(grant, is_reminder=True)

    messages.add_message(request, messages.INFO, "Grants reminder sent")


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
            "approved_amount",
            "full_name",
            "conference",
            "user_id",
            "email",
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
        )


@admin.register(Grant)
class GrantAdmin(ExportMixin, AdminUsersMixin, SearchUsersMixin):
    resource_class = GrantResource
    form = GrantAdminForm
    list_display = (
        "user_display_name",
        "conference",
        "status",
        "approved_type",
        "approved_amount",
        "applicant_reply_sent_at",
        "applicant_reply_deadline",
    )
    readonly_fields = ("email",)
    list_filter = (
        "conference",
        "occupation",
        "grant_type",
        "interested_in_volunteering",
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
        "delete_selected",
    ]

    @admin.display(
        description="User",
    )
    def user_display_name(self, obj):
        if obj.user_id:
            return self.get_user_display_name(obj.user_id)
        return obj.email

    class Media:
        js = ["admin/js/jquery.init.js"]
