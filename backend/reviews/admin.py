from django import forms
from django.contrib import admin
from django.http.request import HttpRequest
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from users.admin_mixins import ConferencePermissionMixin
from reviews.models import AvailableScoreOption, ReviewSession, UserReview
from reviews.admin_mixins import ReviewSessionAdminMixin, ReviewSessionViewMixin
from reviews.services import ReviewSessionService
from submissions.models import SubmissionTag


class AvailableScoreOptionInline(admin.TabularInline):
    model = AvailableScoreOption

    def get_readonly_fields(self, request: HttpRequest, obj):
        if obj and not obj.is_draft:
            return ["numeric_value", "label"]

        return super().get_readonly_fields(request, obj)


def get_all_tags():
    return SubmissionTag.objects.values_list("id", "name")


class SubmitVoteForm(forms.Form):
    score = forms.ModelChoiceField(queryset=AvailableScoreOption.objects.all())
    comment = forms.CharField(required=False)
    private_comment = forms.CharField(required=False)
    exclude = forms.MultipleChoiceField(choices=get_all_tags, required=False)
    seen = forms.CharField(required=False)
    _next = forms.CharField(required=False)
    _skip = forms.CharField(required=False)


@admin.register(UserReview)
class UserReviewAdmin(admin.ModelAdmin):
    list_display = ("edit_vote", "object", "score", "review_session")
    list_filter = ("review_session",)
    list_display_links = ()
    autocomplete_fields = (
        "user",
        "proposal",
        "grant",
    )

    def object(self, obj):
        return obj.get_object()

    def edit_vote(self, obj):
        url = reverse(
            "admin:reviews-vote-view",
            kwargs={
                "review_session_id": obj.review_session_id,
                "review_item_id": obj.object_id,
            },
        )
        return mark_safe(f'<a href="{url}">Edit your vote</a>')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_id=request.user.id).prefetch_related("proposal", "grant")


class ReviewSessionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")

        if instance and "status" in self.fields:
            choices = ReviewSession.Status.choices
            if instance.is_reviewing and instance.has_user_reviews:
                choices = ReviewSession.Status.choices[1:]

            self.fields["status"].choices = choices


@admin.register(ReviewSession)
class ReviewSessionAdmin(
    ReviewSessionAdminMixin,
    ReviewSessionViewMixin,
    ConferencePermissionMixin,
    admin.ModelAdmin,
):
    form = ReviewSessionForm
    inlines = [
        AvailableScoreOptionInline,
    ]

    def get_fieldsets(self, request: HttpRequest, obj):
        goto_fieldset = (
            "Go To",
            {
                "fields": (
                    "go_to_review_screen",
                    "go_to_recap_screen",
                )
            },
        )
        config_fieldset = (
            "Config",
            {
                "fields": (
                    "session_type",
                    "conference",
                    "status",
                )
            },
        )

        if obj:
            fieldsets = (goto_fieldset, config_fieldset)
        else:
            fieldsets = (config_fieldset,)

        return fieldsets

    def get_readonly_fields(self, request: HttpRequest, obj):
        fields = [
            "go_to_review_screen",
            "go_to_recap_screen",
        ]

        if obj:
            if not obj.is_draft:
                fields += [
                    "session_type",
                    "conference",
                ]

            if obj.is_completed and obj.has_user_reviews:
                fields += [
                    "status",
                ]

        if not obj:
            fields += [
                "status",
            ]

        return fields

    def get_urls(self):
        return [
            path(
                "<int:review_session_id>/review/recap/",
                self.admin_site.admin_view(self.review_recap_view),
                name="reviews-recap",
            ),
            path(
                "<int:review_session_id>/review/start/",
                self.admin_site.admin_view(self.review_start_view),
                name="reviews-start",
            ),
            path(
                "<int:review_session_id>/review/<int:review_item_id>/",
                self.admin_site.admin_view(self.review_view),
                name="reviews-vote-view",
            ),
        ] + super().get_urls()


# Legacy function kept for backward compatibility
def get_next_to_review_item_id(
    review_session: ReviewSession,
    user,
    skip_item: int | None = None,
    exclude: list[int] = None,
    seen: list[int] = None,
) -> int | None:
    """Legacy function - use ReviewSessionService.get_next_item_to_review instead."""
    service = ReviewSessionService(review_session)
    return service.get_next_item_to_review(user, skip_item, exclude, seen)
