from dal_admin_filters import AutocompleteFilter
from django.contrib import admin
from voting.models import RankRequest, Vote


class UserFilter(AutocompleteFilter):
    title = "Author"
    field_name = "user"
    autocomplete_url = "user-autocomplete"


class SubmissionFilter(AutocompleteFilter):
    title = "Submission"
    field_name = "submission"
    autocomplete_url = "submission-autocomplete"


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("submission", "user", "value")
    list_filter = (SubmissionFilter, UserFilter, "value")
    search_fields = (
        "submission__title",
        "user__name",
        "user__full_name",
        "user__email",
    )

    class Media:
        js = ["admin/js/jquery.init.js"]


@admin.register(RankRequest)
class RankRequestAdmin(admin.ModelAdmin):
    list_display = ("conference", "created")
