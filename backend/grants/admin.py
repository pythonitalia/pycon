from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.fields import Field

from submissions.models import Submission
from users.mixins import ResourceUsersByEmailsMixin

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
    "conference__code",
    "created",
)


class GrantResource(ResourceUsersByEmailsMixin):
    search_field = "email"
    has_sent_submission = Field()
    submission_title = Field()
    USERS_SUBMISSIONS = {}

    def dehydrate_has_sent_submission(self, obj):
        return "yes" if obj.email in self.USERS_SUBMISSIONS else "no"

    def dehydrate_submission_title(self, obj):
        return self.USERS_SUBMISSIONS.get(obj.email, "")

    def before_export(self, queryset, *args, **kwargs):
        super().before_export(queryset, *args, **kwargs)
        ids = {u["id"]: u["email"] for u in self._PREFETCHED_USERS_BY_EMAIL.values()}
        submissions = Submission.objects.filter(speaker_id__in=ids.keys())

        self.USERS_SUBMISSIONS = {ids[str(s.speaker_id)]: s.title for s in submissions}
        return queryset

    class Meta:
        model = Grant
        fields = EXPORT_GRANTS_FIELDS
        export_order = EXPORT_GRANTS_FIELDS


@admin.register(Grant)
class GrantAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = GrantResource
    list_display = (
        "email",
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
