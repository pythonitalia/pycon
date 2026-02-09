import urllib.parse

from django import forms
from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from reviews.adapters import get_review_adapter
from reviews.models import AvailableScoreOption, ReviewSession, UserReview
from submissions.models import Submission, SubmissionTag
from users.admin_mixins import ConferencePermissionMixin


def get_accepted_submissions(conference):
    return (
        Submission.objects.filter(conference=conference)
        .filter(
            Q(pending_status=Submission.STATUS.accepted)
            | Q(pending_status__isnull=True, status=Submission.STATUS.accepted)
            | Q(pending_status="", status=Submission.STATUS.accepted)
        )
        .select_related("speaker", "type", "audience_level")
        .prefetch_related("languages")
    )


class AvailableScoreOptionInline(admin.TabularInline):
    model = AvailableScoreOption

    def get_readonly_fields(self, request: HttpRequest, obj):
        if obj and not obj.is_draft:
            return ["numeric_value", "label"]

        return super().get_readonly_fields(request, obj)


def get_all_tags():
    # todo improve :)
    return SubmissionTag.objects.values_list("id", "name")


def get_stats_for_submissions(qs):
    """Get all stats for a queryset of submissions."""
    total = qs.count()

    def calc_pct(count):
        return round(count / total * 100, 1) if total > 0 else 0

    def with_pct(counts_dict):
        return {k: (v, calc_pct(v)) for k, v in counts_dict.items()}

    gender_stats = (
        qs.values("speaker__gender")
        .annotate(count=Count("id"))
        .order_by("speaker__gender")
    )
    gender_counts = with_pct(
        {
            item["speaker__gender"] or "unknown": item["count"]
            for item in gender_stats
        }
    )

    level_stats = (
        qs.values("audience_level__name")
        .annotate(count=Count("id"))
        .order_by("audience_level__name")
    )
    level_counts = with_pct(
        {item["audience_level__name"]: item["count"] for item in level_stats}
    )

    language_stats = (
        qs.values("languages__code")
        .annotate(count=Count("id"))
        .order_by("languages__code")
    )
    language_counts = with_pct(
        {item["languages__code"]: item["count"] for item in language_stats}
    )

    speaker_level_stats = (
        qs.values("speaker_level")
        .annotate(count=Count("id"))
        .order_by("speaker_level")
    )
    speaker_level_counts = with_pct(
        {item["speaker_level"]: item["count"] for item in speaker_level_stats}
    )

    tag_stats = (
        qs.values("tags__name")
        .annotate(count=Count("id"))
        .exclude(tags__name__isnull=True)
        .order_by("-count", "tags__name")
    )
    tag_counts = [
        (item["tags__name"], item["count"], calc_pct(item["count"]))
        for item in tag_stats
    ]

    return {
        "total": total,
        "gender_counts": gender_counts,
        "level_counts": level_counts,
        "language_counts": language_counts,
        "speaker_level_counts": speaker_level_counts,
        "tag_counts": tag_counts,
    }


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
                    "go_to_shortlist_screen",
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
            "go_to_shortlist_screen",
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

    @admin.display(description="Shortlist Screen")
    def go_to_shortlist_screen(self, obj):
        if not obj.id:
            return ""

        if not obj.can_see_shortlist_screen:
            return "You cannot see the shortlist of this session yet."

        return mark_safe(
            f"""
    <a href="{reverse("admin:reviews-shortlist", kwargs={"review_session_id": obj.id})}">
        Go to shortlist screen
    </a>
"""
        )

    @admin.display(description="Recap Screen")
    def go_to_recap_screen(self, obj):
        if not obj.id:
            return ""

        if not obj.can_see_shortlist_screen:
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
                "<int:review_session_id>/review/shortlist/",
                self.admin_site.admin_view(self.review_shortlist_view),
                name="reviews-shortlist",
            ),
            path(
                "<int:review_session_id>/review/recap/",
                self.admin_site.admin_view(self.review_recap_view),
                name="reviews-recap",
            ),
            path(
                "<int:review_session_id>/review/recap/compute-analysis/",
                self.admin_site.admin_view(self.review_recap_compute_analysis_view),
                name="reviews-recap-compute-analysis",
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
                    "admin:reviews-shortlist",
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

    def review_shortlist_view(self, request, review_session_id):
        review_session = ReviewSession.objects.get(id=review_session_id)

        if not review_session.user_can_review(request.user):
            raise PermissionDenied()

        if not review_session.can_see_shortlist_screen:
            messages.error(request, "You cannot see the shortlist of this session yet.")
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

            adapter.process_shortlist_post(request, review_session)
            messages.success(request, "Decisions saved.")

            return redirect(
                reverse(
                    "admin:reviews-shortlist",
                    kwargs={
                        "review_session_id": review_session_id,
                    },
                )
            )

        items = adapter.get_shortlist_items_queryset(review_session).all()
        context = adapter.get_shortlist_context(
            request, review_session, items, self.admin_site
        )

        return TemplateResponse(request, adapter.shortlist_template, context)

    def _get_accepted_submissions(self, conference):
        return get_accepted_submissions(conference)

    def review_recap_view(self, request, review_session_id):
        review_session = ReviewSession.objects.get(id=review_session_id)

        if not review_session.user_can_review(request.user):
            raise PermissionDenied()

        if not review_session.can_see_shortlist_screen:
            messages.error(request, "You cannot see the recap of this session yet.")
            return redirect(
                reverse(
                    "admin:reviews_reviewsession_change",
                    kwargs={
                        "object_id": review_session_id,
                    },
                )
            )

        conference = review_session.conference
        accepted_submissions = self._get_accepted_submissions(conference)

        # Get submission types for this conference
        submission_types = list(
            conference.submission_types.values_list("name", flat=True)
        )

        # Get stats per submission type
        stats_by_type = {}
        for type_name in submission_types:
            type_qs = accepted_submissions.filter(type__name=type_name)
            stats_by_type[type_name] = get_stats_for_submissions(type_qs)

        total_accepted = accepted_submissions.count()

        # Build submissions data for JS to use when rendering analysis results
        submissions_data = [
            {
                "id": s.id,
                "title": str(s.title),
                "type": s.type.name,
                "speaker": s.speaker.display_name if s.speaker else "Unknown",
            }
            for s in accepted_submissions
        ]

        context = dict(
            self.admin_site.each_context(request),
            title="Recap",
            review_session_id=review_session_id,
            review_session_repr=str(review_session),
            total_accepted=total_accepted,
            submission_types=submission_types,
            stats_by_type=stats_by_type,
            submissions_data=submissions_data,
            compute_analysis_url=reverse(
                "admin:reviews-recap-compute-analysis",
                kwargs={"review_session_id": review_session_id},
            ),
        )

        return TemplateResponse(request, "reviews-recap.html", context)

    def review_recap_compute_analysis_view(self, request, review_session_id):
        review_session = ReviewSession.objects.get(id=review_session_id)

        if not review_session.user_can_review(request.user):
            raise PermissionDenied()

        if not review_session.can_see_shortlist_screen:
            raise PermissionDenied()

        conference = review_session.conference
        accepted_submissions = list(self._get_accepted_submissions(conference))
        force_recompute = request.GET.get("recompute") == "1"

        from django.core.cache import cache

        from pycon.tasks import check_pending_heavy_processing_work
        from reviews.similar_talks import _get_cache_key
        from reviews.tasks import compute_recap_analysis

        combined_cache_key = _get_cache_key(
            "recap_analysis", conference.id, accepted_submissions
        )

        if not force_recompute:
            cached_result = cache.get(combined_cache_key)
            if cached_result is not None:
                return JsonResponse(cached_result)

        # Use cache.add as a lock to prevent duplicate task dispatch
        computing_key = f"{combined_cache_key}:computing"
        if cache.add(computing_key, True, timeout=600):
            compute_recap_analysis.apply_async(
                args=[conference.id, combined_cache_key],
                kwargs={"force_recompute": force_recompute},
                queue="heavy_processing",
            )
            check_pending_heavy_processing_work.delay()

        return JsonResponse({"status": "processing"})

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
                        "admin:reviews-shortlist",
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
