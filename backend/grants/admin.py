from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.fields import Field

from submissions.models import Submission
from users.mixins import AdminUsersMixin, ResourceUsersByEmailsMixin, SearchUsersMixin

from .models import Grant

EXPORT_GRANTS_FIELDS = (
    "name",
    "full_name",
    "email",
    "age",
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


class GrantResource(ResourceUsersByEmailsMixin):
    search_field = "email"
    has_sent_submission = Field()
    submission_title = Field()
    submission_admin_link = Field()
    submission_pycon_link = Field()
    USERS_SUBMISSIONS = {}

    def dehydrate_has_sent_submission(self, obj):
        return "yes" if obj.email in self.USERS_SUBMISSIONS else "no"

    def dehydrate_submission_title(self, obj):
        submissions = self.USERS_SUBMISSIONS.get(obj.email)
        if not submissions:
            return
        return "\n".join([s.title for s in submissions])

    def dehydrate_submission_pycon_link(self, obj):
        submissions = self.USERS_SUBMISSIONS.get(obj.email)
        if not submissions:
            return
        return "\n".join(
            [f"https://pycon.it/submission/{s.hashid}" for s in submissions]
        )

    def dehydrate_submission_admin_link(self, obj):
        submissions = self.USERS_SUBMISSIONS.get(obj.email)
        if not submissions:
            return
        return "\n".join(
            [
                f"https://admin.pycon.it/admin/submissions/submission/{s.id}/change/"
                for s in submissions
            ]
        )

    def before_export(self, queryset, *args, **kwargs):
        super().before_export(queryset, *args, **kwargs)
        users_ids = {
            u["id"]: u["email"] for u in self._PREFETCHED_USERS_BY_EMAIL.values()
        }
        submissions = Submission.objects.filter(speaker_id__in=users_ids.keys())

        self.USERS_SUBMISSIONS = {}
        for submission in submissions:
            user_email = users_ids[str(submission.speaker_id)]
            self.USERS_SUBMISSIONS.setdefault(user_email, [])

            self.USERS_SUBMISSIONS[user_email].append(submission)

        return queryset

    class Meta:
        model = Grant
        fields = EXPORT_GRANTS_FIELDS
        export_order = EXPORT_GRANTS_FIELDS


@admin.register(Grant)
class GrantAdmin(ExportMixin, AdminUsersMixin, SearchUsersMixin):
    resource_class = GrantResource
    list_display = (
        "user_display_name",
        "full_name",
        "conference",
        "travelling_from",
        "age",
        "gender",
        "occupation",
        "grant_type",
        "python_usage",
        "been_to_other_events",
        "interested_in_volunteering",
        "needs_funds_for_travel",
        "why",
        "notes",
    )

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

    def user_display_name(self, obj):
        if obj.user_id:
            return self.get_user_display_name(obj.user_id)
        return obj.email

    user_display_name.short_description = "User"
