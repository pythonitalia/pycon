import urllib.parse

from django import forms
from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from reviews.adapters import get_review_adapter
from reviews.models import AvailableScoreOption, ReviewSession, UserReview
from submissions.models import SubmissionTag
from users.admin_mixins import ConferencePermissionMixin


class AvailableScoreOptionInline(admin.TabularInline):
    model = AvailableScoreOption

    def get_readonly_fields(self, request: HttpRequest, obj):
        if obj and not obj.is_draft:
            return ["numeric_value", "label"]

        return super().get_readonly_fields(request, obj)


def get_all_tags():
    # todo improve :)
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
class ReviewSessionAdmin(ConferencePermissionMixin, admin.ModelAdmin):
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

    @admin.display(description="Review Item Screen")
    def go_to_review_screen(self, obj):
        if not obj.id:
            return ""

        if not obj.can_review_items:
            return "You cannot review."

        return mark_safe(
            f"""
    <a href="{reverse("admin:reviews-start", kwargs={"review_session_id": obj.id})}">
        Go to review screen
    </a>
"""
        )

    @admin.display(description="Recap Screen")
    def go_to_recap_screen(self, obj):
        if not obj.id:
            return ""

        if not obj.can_see_recap_screen:
            return "You cannot see the recap of this session yet."

        return mark_safe(
            f"""
    <a href="{reverse("admin:reviews-recap", kwargs={"review_session_id": obj.id})}">
        Go to recap screen
    </a>
"""
        )

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

    def review_start_view(self, request, review_session_id):
        review_session = ReviewSession.objects.get(id=review_session_id)
        adapter = get_review_adapter(review_session)
        next_to_review = adapter.get_next_to_review_item_id(
            review_session, request.user
        )

        if not next_to_review:
            messages.warning(request, "No new proposal to review.")
            return redirect(
                reverse(
                    "admin:reviews-recap",
                    kwargs={
                        "review_session_id": review_session_id,
                    },
                )
            )

        return redirect(
            reverse(
                "admin:reviews-vote-view",
                kwargs={
                    "review_session_id": review_session_id,
                    "review_item_id": next_to_review,
                },
            )
        )

    def review_recap_view(self, request, review_session_id):
        review_session = ReviewSession.objects.get(id=review_session_id)

        if not review_session.user_can_review(request.user):
            raise PermissionDenied()

        if not review_session.can_see_recap_screen:
            messages.error(request, "You cannot see the recap of this session yet.")
            return redirect(
                reverse(
                    "admin:reviews_reviewsession_change",
                    kwargs={
                        "object_id": review_session_id,
                    },
                )
            )

        adapter = get_review_adapter(review_session)

        if request.method == "POST":
            if not request.user.has_perm(
                "reviews.decision_reviewsession", review_session
            ):
                raise PermissionDenied()

            adapter.process_recap_post(request, review_session)

            if review_session.is_grants_review:
                messages.success(
                    request, "Decisions saved. Check the Grants Summary for more info."
                )

            return redirect(
                reverse(
                    "admin:reviews-recap",
                    kwargs={
                        "review_session_id": review_session_id,
                    },
                )
            )

        items = adapter.get_recap_items_queryset(review_session).all()
        context = adapter.get_recap_context(
            request, review_session, items, self.admin_site
        )

        return TemplateResponse(request, adapter.recap_template, context)

    def review_view(self, request, review_session_id, review_item_id):
        review_session = ReviewSession.objects.get(id=review_session_id)

        if not review_session.user_can_review(request.user):
            raise PermissionDenied()

        adapter = get_review_adapter(review_session)

        if request.method == "GET":
            filter_options = adapter.get_user_review_filter(review_item_id)
            user_review = UserReview.objects.filter(
                user_id=request.user.id,
                review_session_id=review_session_id,
                **filter_options,
            ).first()

            context = adapter.get_review_context(
                request,
                review_session,
                review_item_id,
                user_review,
                self.admin_site,
            )
            return TemplateResponse(request, adapter.review_template, context)

        # POST request handling
        form = SubmitVoteForm(request.POST)
        form.is_valid()

        seen = [str(id_) for id_ in form.cleaned_data.get("seen", "").split(",") if id_]
        seen.append(str(review_item_id))

        exclude = form.cleaned_data.get("exclude", [])

        next_to_review = None

        if form.cleaned_data.get("_skip"):
            # Skipping to the next item without voting
            next_to_review = adapter.get_next_to_review_item_id(
                review_session,
                request.user,
                skip_item=review_item_id,
                exclude=exclude,
                seen=seen,
            )
        elif form.cleaned_data.get("_next"):
            if not form.is_valid():
                messages.error(request, "Invalid vote")
                comment = urllib.parse.quote(form.cleaned_data["comment"])
                private_comment = urllib.parse.quote(
                    form.cleaned_data["private_comment"]
                )

                return redirect(
                    reverse(
                        "admin:reviews-vote-view",
                        kwargs={
                            "review_session_id": review_session_id,
                            "review_item_id": review_item_id,
                        },
                    )
                    + f"?exclude={','.join(exclude)}"
                    + f"&seen={','.join(seen)}"
                    + f"&comment={comment}"
                    + f"&private_comment={private_comment}"
                )

            values = {
                "user_id": request.user.id,
                "review_session_id": review_session_id,
                **adapter.get_user_review_create_values(review_item_id),
            }

            UserReview.objects.update_or_create(
                **values,
                defaults={
                    "score_id": form.cleaned_data["score"].id,
                    "comment": form.cleaned_data["comment"],
                    "private_comment": form.cleaned_data["private_comment"],
                },
            )
            next_to_review = adapter.get_next_to_review_item_id(
                review_session, request.user, exclude=exclude, seen=seen
            )

        if not next_to_review:
            messages.warning(
                request, "No new items to review, showing an already seen one."
            )
            next_to_review = adapter.get_next_to_review_item_id(
                review_session,
                request.user,
                skip_item=review_item_id,
                exclude=exclude,
            )

            if not next_to_review:
                messages.warning(request, "No new proposal to review.")
                return redirect(
                    reverse(
                        "admin:reviews-recap",
                        kwargs={
                            "review_session_id": review_session_id,
                        },
                    )
                )

        return redirect(
            reverse(
                "admin:reviews-vote-view",
                kwargs={
                    "review_session_id": review_session_id,
                    "review_item_id": next_to_review,
                },
            )
            + f"?exclude={','.join(exclude)}&seen={','.join(seen)}"
        )
