from typing import Any, Dict, List, Optional

from django.db import models
from django.db.models import Q, Count, F, Avg, Sum, Exists, OuterRef, Prefetch
from django.db.models.expressions import ExpressionWrapper
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.contrib.postgres.expressions import ArraySubquery
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import HttpRequest

from reviews.interfaces import ReviewStrategy
from reviews.models import ReviewSession, UserReview


class ProposalReviewStrategy(ReviewStrategy):
    """Strategy for reviewing proposals/submissions."""

    def get_reviewable_items_queryset(
        self, review_session: ReviewSession
    ) -> models.QuerySet:
        from submissions.models import Submission

        return Submission.objects.for_conference(
            review_session.conference_id
        ).non_cancelled()

    def get_next_item_to_review(
        self,
        review_session: ReviewSession,
        user,
        skip_item: Optional[int] = None,
        exclude: Optional[List[int]] = None,
        seen: Optional[List[int]] = None,
    ) -> Optional[int]:
        exclude = exclude or []
        seen = seen or []

        already_reviewed = UserReview.objects.filter(
            user_id=user.id,
            review_session_id=review_session.id,
        )
        already_reviewed_ids = already_reviewed.values_list("proposal_id", flat=True)

        skip_item_array = [skip_item] if skip_item else []
        seen_items_to_ignore = list(already_reviewed_ids) + skip_item_array + seen

        qs = (
            self.get_reviewable_items_queryset(review_session)
            .annotate(
                votes_received=Count(
                    "userreview",
                    filter=Q(userreview__review_session_id=review_session.id),
                )
            )
            .order_by("votes_received", "?")
        )

        if seen_items_to_ignore:
            qs = qs.exclude(id__in=seen_items_to_ignore)

        if exclude:
            qs = qs.exclude(tags__in=exclude)

        unvoted_item = qs.first()
        return unvoted_item.id if unvoted_item else None

    def get_review_template_name(self) -> str:
        return "reviews/proposal-review.html"

    def get_recap_template_name(self) -> str:
        return "proposals-recap.html"

    def process_review_decisions(
        self, request: HttpRequest, review_session: ReviewSession
    ) -> None:
        if not request.user.has_perm("reviews.decision_reviewsession", review_session):
            raise PermissionDenied()

        data = request.POST
        decisions = {
            int(key.split("-")[1]): value
            for [key, value] in data.items()
            if key.startswith("decision-")
        }

        from submissions.models import Submission

        proposals = list(
            review_session.conference.submissions.filter(id__in=decisions.keys()).all()
        )

        for proposal in proposals:
            decision = decisions[proposal.id]
            proposal.pending_status = decision

        Submission.objects.bulk_update(
            proposals,
            fields=["pending_status"],
        )

    def get_recap_context_data(
        self, request: HttpRequest, review_session: ReviewSession
    ) -> Dict[str, Any]:
        from submissions.models import Submission
        from grants.models import Grant

        items = (
            Submission.objects.for_conference(review_session.conference_id)
            .non_cancelled()
            .annotate(
                score=models.Subquery(
                    UserReview.objects.select_related("score")
                    .filter(
                        review_session_id=review_session.id,
                        proposal_id=OuterRef("id"),
                    )
                    .values("proposal_id")
                    .annotate(score=Avg("score__numeric_value"))
                    .values("score")
                )
            )
            .order_by(F("score").desc(nulls_last=True))
            .prefetch_related(
                Prefetch(
                    "userreview_set",
                    queryset=UserReview.objects.prefetch_related(
                        "user", "score"
                    ).filter(review_session_id=review_session.id),
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
                conference=review_session.conference, user_id__in=speakers_ids
            ).all()
        }

        return {
            "items": items,
            "grants": grants,
            "audience_levels": review_session.conference.audience_levels.all(),
            "all_statuses": [choice for choice in Submission.STATUS],
        }

    def validate_user_review_data(self, data: Dict[str, Any]) -> bool:
        required_fields = ["score"]
        return all(field in data for field in required_fields)

    def create_user_review_fields(self, review_item_id: int) -> Dict[str, Any]:
        return {"proposal_id": review_item_id}


class GrantReviewStrategy(ReviewStrategy):
    """Strategy for reviewing grants."""

    def get_reviewable_items_queryset(
        self, review_session: ReviewSession
    ) -> models.QuerySet:
        return review_session.conference.grants.all()

    def get_next_item_to_review(
        self,
        review_session: ReviewSession,
        user,
        skip_item: Optional[int] = None,
        exclude: Optional[List[int]] = None,
        seen: Optional[List[int]] = None,
    ) -> Optional[int]:
        exclude = exclude or []
        seen = seen or []

        already_reviewed = UserReview.objects.filter(
            user_id=user.id,
            review_session_id=review_session.id,
        )
        already_reviewed_ids = already_reviewed.values_list("grant_id", flat=True)

        unvoted_item = (
            self.get_reviewable_items_queryset(review_session)
            .annotate(
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

    def get_review_template_name(self) -> str:
        return "reviews/grant-review.html"

    def get_recap_template_name(self) -> str:
        return "grants-recap.html"

    def process_review_decisions(
        self, request: HttpRequest, review_session: ReviewSession
    ) -> None:
        if not request.user.has_perm("reviews.decision_reviewsession", review_session):
            raise PermissionDenied()

        data = request.POST
        decisions = {
            int(key.split("-")[1]): value
            for [key, value] in data.items()
            if key.startswith("decision-")
        }

        approved_type_decisions = {
            int(key.split("-")[1]): value
            for [key, value] in data.items()
            if key.startswith("approvedtype-")
        }

        from grants.models import Grant

        grants = list(
            review_session.conference.grants.filter(id__in=decisions.keys()).all()
        )

        for grant in grants:
            decision = decisions[grant.id]
            if decision not in Grant.REVIEW_SESSION_STATUSES_OPTIONS:
                continue

            approved_type = approved_type_decisions.get(grant.id, "")

            if decision != grant.status:
                grant.pending_status = decision
            elif decision == grant.status:
                grant.pending_status = None

            grant.approved_type = (
                approved_type if decision == Grant.Status.approved else None
            )

        for grant in grants:
            grant.save(update_fields=["pending_status", "approved_type"])

        messages.success(
            request, "Decisions saved. Check the Grants Summary for more info."
        )

    def get_recap_context_data(
        self, request: HttpRequest, review_session: ReviewSession
    ) -> Dict[str, Any]:
        from submissions.models import Submission
        from grants.models import Grant

        items = (
            review_session.conference.grants.annotate(
                total_score=Cast(
                    Sum(
                        "userreview__score__numeric_value",
                        filter=Q(userreview__review_session_id=review_session.id),
                    ),
                    output_field=FloatField(),
                ),
                vote_count=Cast(
                    Count(
                        "userreview",
                        filter=Q(userreview__review_session_id=review_session.id),
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
                    ).filter(review_session_id=review_session.id),
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

        return {
            "items": items,
            "proposals": proposals,
            "all_review_statuses": [
                choice
                for choice in Grant.Status.choices
                if choice[0] in Grant.REVIEW_SESSION_STATUSES_OPTIONS
            ],
            "all_statuses": Grant.Status.choices,
            "all_approved_types": [choice for choice in Grant.ApprovedType.choices],
        }

    def validate_user_review_data(self, data: Dict[str, Any]) -> bool:
        required_fields = ["score"]
        return all(field in data for field in required_fields)

    def create_user_review_fields(self, review_item_id: int) -> Dict[str, Any]:
        return {"grant_id": review_item_id}


class ReviewStrategyFactory:
    """Factory for creating appropriate review strategies."""

    _strategies = {
        ReviewSession.SessionType.PROPOSALS: ProposalReviewStrategy,
        ReviewSession.SessionType.GRANTS: GrantReviewStrategy,
    }

    @classmethod
    def get_strategy(cls, session_type: str) -> ReviewStrategy:
        """Get the appropriate strategy for the given session type."""
        strategy_class = cls._strategies.get(session_type)
        if not strategy_class:
            raise ValueError(f"No strategy found for session type: {session_type}")
        return strategy_class()

    @classmethod
    def register_strategy(cls, session_type: str, strategy_class: type) -> None:
        """Register a new strategy for a session type."""
        cls._strategies[session_type] = strategy_class
