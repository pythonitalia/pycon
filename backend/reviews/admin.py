from django.contrib.postgres.expressions import ArraySubquery
from django.db.models.expressions import ExpressionWrapper
from django.db.models import FloatField
from django.db.models.functions import Cast
from users.admin_mixins import ConferencePermissionMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Exists
import urllib.parse
from typing import List, Optional

from django import forms
from django.contrib import admin, messages
from django.db.models import Count, F, OuterRef, Prefetch, Subquery, Sum
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from grants.models import Grant
from participants.models import Participant
from reviews.models import AvailableScoreOption, ReviewSession, UserReview
from submissions.models import Submission, SubmissionTag
from users.models import User


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
    <a href="{reverse('admin:reviews-start', kwargs={'review_session_id': obj.id})}">
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
    <a href="{reverse('admin:reviews-recap', kwargs={'review_session_id': obj.id})}">
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
        next_to_review = get_next_to_review_item_id(review_session, request.user)

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

        if review_session.is_proposals_review:
            return self._review_proposals_recap_view(request, review_session)

        if review_session.is_grants_review:
            return self._review_grants_recap_view(request, review_session)

    def _review_grants_recap_view(self, request, review_session):
        review_session_id = review_session.id

        if request.method == "POST":
            if not request.user.has_perm(
                "reviews.decision_reviewsession", review_session
            ):
                raise PermissionDenied()
            data = request.POST

            decisions = {
                int(key.split("-")[1]): value
                for [key, value] in data.items()
                if key.startswith("decision-")
            }

            grants = list(
                review_session.conference.grants.filter(id__in=decisions.keys()).all()
            )

            for grant in grants:
                decision = decisions[grant.id]
                if decision not in Grant.REVIEW_SESSION_STATUSES_OPTIONS:
                    continue

                grant.status = decision

            Grant.objects.bulk_update(
                grants,
                fields=["status"],
            )

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

        items = (
            review_session.conference.grants.annotate(
                total_score=Cast(
                    Sum(
                        "userreview__score__numeric_value",
                        filter=Q(userreview__review_session_id=review_session_id),
                    ),
                    output_field=FloatField(),
                ),
                vote_count=Cast(
                    Count(
                        "userreview",
                        filter=Q(userreview__review_session_id=review_session_id),
                    ),
                    output_field=FloatField(),
                ),
                score=ExpressionWrapper(
                    F("total_score") / F("vote_count"),
                    output_field=FloatField(),
                ),
                has_sent_a_proposal=Exists(
                    Submission.objects.non_cancelled().filter(
                        speaker_id=OuterRef("user_id"),
                        conference_id=review_session.conference_id,
                    )
                ),
                proposals_ids=ArraySubquery(
                    Submission.objects.non_cancelled()
                    .filter(
                        speaker_id=OuterRef("user_id"),
                        conference_id=review_session.conference_id,
                    )
                    .values("id")
                ),
            )
            .order_by(F("score").desc(nulls_last=True))
            .prefetch_related(
                Prefetch(
                    "userreview_set",
                    queryset=UserReview.objects.prefetch_related(
                        "user", "score"
                    ).filter(review_session_id=review_session_id),
                ),
                "user",
            )
            .all()
        )

        proposals = {
            submission.id: submission
            for submission in Submission.objects.non_cancelled()
            .filter(
                conference_id=review_session.conference_id,
                speaker_id__in=items.values_list("user_id"),
            )
            .prefetch_related("rankings", "rankings__tag")
        }

        context = dict(
            self.admin_site.each_context(request),
            request=request,
            items=items,
            proposals=proposals,
            review_session_id=review_session_id,
            review_session_repr=str(review_session),
            all_statuses=[
                choice
                for choice in Grant.Status.choices
                if choice[0] in Grant.REVIEW_SESSION_STATUSES_OPTIONS
            ],
            title="Recap",
        )
        return TemplateResponse(request, "grants-recap.html", context)

    def _review_proposals_recap_view(self, request, review_session):
        review_session_id = review_session.id
        conference = review_session.conference

        if request.method == "POST":
            if not request.user.has_perm(
                "reviews.decision_reviewsession", review_session
            ):
                raise PermissionDenied()

            data = request.POST

            decisions = {
                int(key.split("-")[1]): value
                for [key, value] in data.items()
                if key.startswith("decision-")
            }

            proposals = list(
                conference.submissions.filter(id__in=decisions.keys()).all()
            )

            for proposal in proposals:
                decision = decisions[proposal.id]

                if decision == "accept":
                    proposal.status = Submission.STATUS.accepted
                elif decision == "reject":
                    proposal.status = Submission.STATUS.rejected

            Submission.objects.bulk_update(
                proposals,
                fields=["status"],
            )

            return redirect(
                reverse(
                    "admin:reviews-recap",
                    kwargs={
                        "review_session_id": review_session_id,
                    },
                )
            )

        items = (
            review_session.conference.submissions.annotate(
                score=Subquery(
                    UserReview.objects.select_related("score")
                    .filter(
                        review_session_id=review_session_id,
                        proposal_id=OuterRef("id"),
                    )
                    .values("proposal_id")
                    .annotate(score=Sum("score__numeric_value"))
                    .values("score")
                )
            )
            .order_by(F("score").desc(nulls_last=True))
            .prefetch_related(
                Prefetch(
                    "userreview_set",
                    queryset=UserReview.objects.prefetch_related(
                        "user", "score"
                    ).filter(review_session_id=review_session_id),
                ),
                "duration",
                "audience_level",
                "languages",
                "speaker",
                "tags",
                "type",
                "rankings",
                "rankings__tag",
            )
            .all()
        )

        speakers_ids = items.values_list("speaker_id", flat=True)

        grants = {
            str(grant.user_id): grant
            for grant in Grant.objects.filter(
                conference=conference, user_id__in=speakers_ids
            ).all()
        }

        context = dict(
            self.admin_site.each_context(request),
            items=items,
            grants=grants,
            review_session_id=review_session_id,
            audience_levels=conference.audience_levels.all(),
            review_session_repr=str(review_session),
            title="Recap",
        )
        return TemplateResponse(request, "proposals-recap.html", context)

    def review_view(self, request, review_session_id, review_item_id):
        review_session = ReviewSession.objects.get(id=review_session_id)

        if not review_session.user_can_review(request.user):
            raise PermissionDenied()

        filter_options = {}

        if review_session.is_proposals_review:
            filter_options["proposal_id"] = review_item_id
        elif review_session.is_grants_review:
            filter_options["grant_id"] = review_item_id

        if request.method == "GET":
            user_review = UserReview.objects.filter(
                user_id=request.user.id,
                review_session_id=review_session_id,
                **filter_options,
            ).first()

            if review_session.is_proposals_review:
                response = self._render_proposal_review(
                    request,
                    review_session=review_session,
                    review_item_id=review_item_id,
                    user_review=user_review,
                )
            elif review_session.is_grants_review:
                response = self._render_grant_review(
                    request,
                    review_session=review_session,
                    review_item_id=review_item_id,
                    user_review=user_review,
                )

            return response
        elif request.method == "POST":
            # if not review_session.can_review_items:
            #     messages.error(request, "You cannot vote yet/anymore.")
            #     return redirect(
            #         reverse(
            #             "admin:reviews_reviewsession_change",
            #             kwargs={
            #                 "object_id": review_session_id,
            #             },
            #         )
            #     )

            form = SubmitVoteForm(request.POST)
            form.is_valid()

            seen = [
                str(id_) for id_ in form.cleaned_data.get("seen", "").split(",") if id_
            ]
            seen.append(str(review_item_id))

            exclude = form.cleaned_data.get("exclude", [])

            if form.cleaned_data.get("_skip"):
                # Skipping to the next item without voting
                next_to_review = get_next_to_review_item_id(
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
                }

                if review_session.is_proposals_review:
                    values["proposal_id"] = review_item_id
                elif review_session.is_grants_review:
                    values["grant_id"] = review_item_id

                UserReview.objects.update_or_create(
                    **values,
                    defaults={
                        "score_id": form.cleaned_data["score"].id,
                        "comment": form.cleaned_data["comment"],
                        "private_comment": form.cleaned_data["private_comment"],
                    },
                )
                next_to_review = get_next_to_review_item_id(
                    review_session, request.user, exclude=exclude, seen=seen
                )

            if not next_to_review:
                messages.warning(
                    request, "No new items to review, showing an already seen one."
                )
                next_to_review = get_next_to_review_item_id(
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

    def _render_grant_review(
        self, request, review_session, review_item_id, user_review
    ):
        private_comment = request.GET.get(
            "private_comment", user_review.private_comment if user_review else ""
        )
        comment = request.GET.get("comment", user_review.comment if user_review else "")

        grant = Grant.objects.get(id=review_item_id)
        context = dict(
            self.admin_site.each_context(request),
            grant=grant,
            has_sent_proposal=Submission.objects.non_cancelled()
            .filter(
                speaker_id=grant.user_id,
                conference_id=grant.conference_id,
            )
            .exists(),
            available_scores=AvailableScoreOption.objects.filter(
                review_session_id=review_session.id
            ).order_by("-numeric_value"),
            review_session_id=review_session.id,
            user_review=user_review,
            private_comment=private_comment,
            comment=comment,
            review_session_repr=str(review_session),
            can_review_items=review_session.can_review_items,
            seen=request.GET.get("seen", "").split(","),
            title=f"Grant Review: {grant.user.display_name}",
        )
        return TemplateResponse(request, "grant-review.html", context)

    def _render_proposal_review(
        self, request, review_session, review_item_id, user_review
    ):
        proposal = Submission.objects.prefetch_related("rankings").get(
            id=review_item_id
        )

        languages = list(proposal.languages.all())
        speaker = proposal.speaker
        grant = Grant.objects.filter(
            conference=proposal.conference_id,
            user_id=proposal.speaker_id,
        ).first()
        grant_link = (
            reverse("admin:grants_grant_change", args=(grant.id,)) if grant else ""
        )

        existing_comment = request.GET.get("comment", "")
        tags_already_excluded = request.GET.get("exclude", "").split(",")

        used_tags = (
            Submission.objects.filter(
                conference_id=proposal.conference_id,
            )
            .values_list("tags__id", flat=True)
            .distinct()
        )

        tags_to_filter = (
            SubmissionTag.objects.filter(id__in=used_tags).order_by("name").all()
        )

        context = dict(
            self.admin_site.each_context(request),
            proposal=proposal,
            languages=proposal.languages.all(),
            available_scores=AvailableScoreOption.objects.filter(
                review_session_id=review_session.id
            ).order_by("-numeric_value"),
            proposal_id=review_item_id,
            review_session_id=review_session.id,
            user_review=user_review,
            has_italian_language=any(
                language for language in languages if language.code == "it"
            ),
            has_english_language=any(
                language for language in languages if language.code == "en"
            ),
            speaker=speaker,
            grant=grant,
            grant_link=grant_link,
            participant=Participant.objects.filter(
                user_id=proposal.speaker_id,
                conference=proposal.conference,
            ).first(),
            tags_to_filter=tags_to_filter,
            tags_already_excluded=tags_already_excluded,
            seen=request.GET.get("seen", "").split(","),
            existing_comment=existing_comment,
            review_session_repr=str(review_session),
            title=f'Proposal Review: {proposal.title.localize("en")}',
        )
        return TemplateResponse(request, "proposal-review.html", context)


def get_next_to_review_item_id(
    review_session: ReviewSession,
    user: User,
    skip_item: Optional[int] = None,
    exclude: List[int] = None,
    seen: List[int] = None,
) -> Optional[int]:
    exclude = exclude or []
    seen = seen or []
    already_reviewed = UserReview.objects.filter(
        user_id=user.id,
        review_session_id=review_session.id,
    )

    if review_session.is_proposals_review:
        already_reviewed_ids = already_reviewed.values_list("proposal_id", flat=True)
        allowed_tags = list(
            SubmissionTag.objects.exclude(id__in=exclude).values_list("id", flat=True)
        )
        skip_item_array = [skip_item] if skip_item else []
        qs = (
            Submission.objects.for_conference(review_session.conference_id)
            .annotate(
                votes_received=Count(
                    "userreview",
                    filter=Q(userreview__review_session_id=review_session.id),
                )
            )
            .filter(tags__in=allowed_tags)
            .exclude(
                id__in=list(already_reviewed_ids) + skip_item_array + seen,
            )
        )
        unvoted_item = qs.first()
    elif review_session.is_grants_review:
        already_reviewed_ids = already_reviewed.values_list("grant_id", flat=True)
        unvoted_item = (
            review_session.conference.grants.annotate(
                votes_received=Count(
                    "userreview",
                    filter=Q(userreview__review_session_id=review_session.id),
                )
            )
            .exclude(
                id__in=list(already_reviewed_ids) + [skip_item] + seen,
            )
            .order_by("votes_received", "?")
            .first()
        )

    return unvoted_item.id if unvoted_item else None
