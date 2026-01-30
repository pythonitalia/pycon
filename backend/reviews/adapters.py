from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import (
    Avg,
    Count,
    Exists,
    F,
    FloatField,
    OuterRef,
    Prefetch,
    Q,
    StdDev,
    Subquery,
    Sum,
)
from django.db.models.expressions import ExpressionWrapper
from django.db.models.functions import Cast
from django.http import HttpRequest
from django.urls import reverse

from custom_admin.audit import (
    create_addition_admin_log_entry,
    create_change_admin_log_entry,
    create_deletion_admin_log_entry,
)
from grants.models import Grant, GrantReimbursement, GrantReimbursementCategory
from participants.models import Participant
from reviews.models import AvailableScoreOption, ReviewSession, UserReview
from submissions.models import Submission, SubmissionTag

if TYPE_CHECKING:
    from django.contrib.admin import AdminSite
    from django.db.models import QuerySet

    from users.models import User


class ReviewAdapter(Protocol):
    """Protocol defining the interface for review type adapters."""

    @property
    def recap_template(self) -> str:
        """Template name for the recap view."""
        ...

    @property
    def review_template(self) -> str:
        """Template name for the individual review view."""
        ...

    def get_recap_items_queryset(
        self,
        review_session: ReviewSession,
    ) -> QuerySet:
        """Return annotated queryset of items for the recap view."""
        ...

    def get_recap_context(
        self,
        request: HttpRequest,
        review_session: ReviewSession,
        items: QuerySet,
        admin_site: AdminSite,
    ) -> dict[str, Any]:
        """Return template context for the recap view."""
        ...

    def process_recap_post(
        self,
        request: HttpRequest,
        review_session: ReviewSession,
    ) -> None:
        """Process and save decisions from the recap form."""
        ...

    def get_review_context(
        self,
        request: HttpRequest,
        review_session: ReviewSession,
        review_item_id: int,
        user_review: UserReview | None,
        admin_site: AdminSite,
    ) -> dict[str, Any]:
        """Return template context for the individual item review view."""
        ...

    def get_next_to_review_item_id(
        self,
        review_session: ReviewSession,
        user: User,
        skip_item: int | None = None,
        exclude: list[int] | None = None,
        seen: list[int] | None = None,
    ) -> int | None:
        """Return the ID of the next unreviewed item, or None if none available."""
        ...

    def get_user_review_filter(self, review_item_id: int) -> dict[str, Any]:
        """Return filter kwargs for finding a user's review of an item."""
        ...

    def get_user_review_create_values(self, review_item_id: int) -> dict[str, Any]:
        """Return values dict for creating/updating a user review."""
        ...


class ProposalsReviewAdapter:
    """Adapter for handling Proposals (Submissions) reviews."""

    @property
    def recap_template(self) -> str:
        return "proposals-recap.html"

    @property
    def review_template(self) -> str:
        return "proposal-review.html"

    def get_recap_items_queryset(
        self,
        review_session: ReviewSession,
    ) -> QuerySet[Submission]:
        """Return submissions annotated with scores for the recap view."""
        review_session_id = review_session.id

        return (
            Submission.objects.for_conference(review_session.conference_id)
            .non_cancelled()
            .annotate(
                score=Subquery(
                    UserReview.objects.select_related("score")
                    .filter(
                        review_session_id=review_session_id,
                        proposal_id=OuterRef("id"),
                    )
                    .values("proposal_id")
                    .annotate(score=Avg("score__numeric_value"))
                    .values("score")
                )
            )
            .order_by(F("score").desc(nulls_last=True), "id")
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
        )

    def get_recap_context(
        self,
        request: HttpRequest,
        review_session: ReviewSession,
        items: QuerySet,
        admin_site: AdminSite,
    ) -> dict[str, Any]:
        """Return template context for the proposals recap view."""
        conference = review_session.conference
        speakers_ids = items.values_list("speaker_id", flat=True)

        grants = {
            str(grant.user_id): grant
            for grant in Grant.objects.filter(
                conference=conference, user_id__in=speakers_ids
            )
        }

        return dict(
            admin_site.each_context(request),
            items=items,
            grants=grants,
            review_session_id=review_session.id,
            audience_levels=conference.audience_levels.all(),
            submission_types=conference.submission_types.all(),
            review_session_repr=str(review_session),
            all_statuses=[choice for choice in Submission.STATUS],
            title="Recap",
        )

    def process_recap_post(
        self,
        request: HttpRequest,
        review_session: ReviewSession,
    ) -> None:
        """Save pending status decisions for proposals."""
        conference = review_session.conference
        data = request.POST

        decisions = {
            int(key.split("-")[1]): value
            for key, value in data.items()
            if key.startswith("decision-")
        }

        proposals = list(conference.submissions.filter(id__in=decisions.keys()))

        for proposal in proposals:
            decision = decisions[proposal.id]
            proposal.pending_status = decision

        Submission.objects.bulk_update(
            proposals,
            fields=["pending_status"],
        )

    def get_review_context(
        self,
        request: HttpRequest,
        review_session: ReviewSession,
        review_item_id: int,
        user_review: UserReview | None,
        admin_site: AdminSite,
    ) -> dict[str, Any]:
        """Return template context for reviewing a single proposal."""
        proposal = (
            Submission.objects.for_conference(review_session.conference_id)
            .prefetch_related(
                "rankings",
                "rankings__tag",
                Prefetch(
                    "userreview_set",
                    queryset=UserReview.objects.prefetch_related(
                        "user", "score"
                    ).filter(review_session_id=review_session.id),
                ),
            )
            .get(id=review_item_id)
        )

        languages = list(proposal.languages.all())
        speaker = proposal.speaker
        grant = (
            Grant.objects.of_user(proposal.speaker_id)
            .for_conference(proposal.conference_id)
            .first()
        )
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

        tags_to_filter = SubmissionTag.objects.filter(id__in=used_tags).order_by("name")

        return dict(
            admin_site.each_context(request),
            proposal=proposal,
            languages=languages,
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
            title=f"Proposal Review: {proposal.title.localize('en')}",
        )

    def get_next_to_review_item_id(
        self,
        review_session: ReviewSession,
        user: User,
        skip_item: int | None = None,
        exclude: list[int] | None = None,
        seen: list[int] | None = None,
    ) -> int | None:
        """Return the next proposal ID to review, prioritising items with fewer votes."""
        exclude = exclude or []
        seen = seen or []

        already_reviewed_ids = UserReview.objects.filter(
            user_id=user.id,
            review_session_id=review_session.id,
        ).values_list("proposal_id", flat=True)

        skip_item_array = [skip_item] if skip_item else []
        seen_items_to_ignore = list(already_reviewed_ids) + skip_item_array + seen

        qs = (
            Submission.objects.non_cancelled()
            .for_conference(review_session.conference_id)
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

    def get_user_review_filter(self, review_item_id: int) -> dict[str, Any]:
        """Return filter kwargs for finding a user's proposal review."""
        return {"proposal_id": review_item_id}

    def get_user_review_create_values(self, review_item_id: int) -> dict[str, Any]:
        """Return values for creating a proposal review."""
        return {"proposal_id": review_item_id}


class GrantsReviewAdapter:
    """Adapter for handling Grants (Financial Aid) reviews."""

    @property
    def recap_template(self) -> str:
        return "grants-recap.html"

    @property
    def review_template(self) -> str:
        return "grant-review.html"

    def get_recap_items_queryset(
        self,
        review_session: ReviewSession,
    ) -> QuerySet[Grant]:
        """Return grants annotated with scores and std_dev for the recap view."""
        review_session_id = review_session.id

        return (
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
                std_dev=StdDev(
                    "userreview__score__numeric_value",
                    filter=Q(userreview__review_session_id=review_session_id),
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
                approved_reimbursement_category_ids=ArraySubquery(
                    GrantReimbursement.objects.filter(
                        grant_id=OuterRef("pk")
                    ).values_list("category_id", flat=True)
                ),
            )
            .order_by(
                F("score").desc(nulls_last=True),  # Score decrescente
                F("std_dev").asc(nulls_first=True),
                "id",
            )
            .prefetch_related(
                Prefetch(
                    "userreview_set",
                    queryset=UserReview.objects.prefetch_related(
                        "user", "score"
                    ).filter(review_session_id=review_session_id),
                ),
                "user",
            )
        )

    def get_recap_context(
        self,
        request: HttpRequest,
        review_session: ReviewSession,
        items: QuerySet,
        admin_site: AdminSite,
    ) -> dict[str, Any]:
        """Return template context for the grants recap view."""
        proposals = {
            submission.id: submission
            for submission in Submission.objects.non_cancelled()
            .filter(
                conference_id=review_session.conference_id,
                speaker_id__in=items.values_list("user_id"),
            )
            .prefetch_related("rankings", "rankings__tag")
        }

        return dict(
            admin_site.each_context(request),
            request=request,
            items=items,
            proposals=proposals,
            review_session_id=review_session.id,
            review_session_repr=str(review_session),
            all_review_statuses=[
                choice
                for choice in Grant.Status.choices
                if choice[0] in Grant.REVIEW_SESSION_STATUSES_OPTIONS
            ],
            all_statuses=Grant.Status.choices,
            all_reimbursement_categories=GrantReimbursementCategory.objects.for_conference(
                conference=review_session.conference
            ),
            review_session=review_session,
            title="Recap",
        )

    def process_recap_post(
        self,
        request: HttpRequest,
        review_session: ReviewSession,
    ) -> None:
        """Save grant decisions, reimbursements, and internal notes."""
        data = request.POST

        reimbursement_categories = {
            category.id: category
            for category in GrantReimbursementCategory.objects.for_conference(
                conference=review_session.conference
            )
        }

        decisions = {
            int(key.split("-")[1]): value
            for key, value in data.items()
            if key.startswith("decision-")
        }

        approved_reimbursement_categories_decisions = {
            int(key.split("-")[1]): [int(id_) for id_ in data.getlist(key)]
            for key in data.keys()
            if key.startswith("reimbursementcategory-")
        }

        notes_updates = {
            int(key.split("-")[1]): value
            for key, value in data.items()
            if key.startswith("notes-")
        }

        grants = list(review_session.conference.grants.filter(id__in=decisions.keys()))

        # Track grants with pending status changes for audit logging
        grants_with_pending_status_changes = {}

        for grant in grants:
            decision = decisions[grant.id]
            if decision not in Grant.REVIEW_SESSION_STATUSES_OPTIONS:
                continue

            original_pending_status = grant.pending_status
            if decision != grant.status:
                grant.pending_status = decision
            elif decision == grant.status:
                grant.pending_status = None

            if grant.pending_status != original_pending_status:
                grants_with_pending_status_changes[grant.id] = original_pending_status

            # Handle reimbursement deletions
            if grant.reimbursements.exists():
                approved_reimbursement_categories = (
                    approved_reimbursement_categories_decisions.get(grant.id, [])
                )
                if decision != Grant.Status.approved:
                    # Delete all reimbursements if not approved
                    for reimbursement in grant.reimbursements.all():
                        create_deletion_admin_log_entry(
                            request.user,
                            grant,
                            change_message=f"[Review Session] Reimbursement removed: {reimbursement.category.name}.",
                        )
                        reimbursement.delete()
                else:
                    # Only keep those in current approved categories
                    to_delete = grant.reimbursements.exclude(
                        category_id__in=approved_reimbursement_categories
                    )
                    for reimbursement in to_delete:
                        create_deletion_admin_log_entry(
                            request.user,
                            grant,
                            change_message=f"[Review Session] Reimbursement removed: {reimbursement.category.name}.",
                        )
                    to_delete.delete()

        # Save grants and create audit logs
        for grant in grants:
            grant.save(update_fields=["pending_status"])

            if grant.id in grants_with_pending_status_changes:
                original_pending_status = grants_with_pending_status_changes[grant.id]
                create_change_admin_log_entry(
                    request.user,
                    grant,
                    change_message=f"[Review Session] Pending status changed from '{original_pending_status}' to '{grant.pending_status}'.",
                )

            # Skip reimbursement creation if not approved
            if grant.pending_status != Grant.Status.approved:
                continue

            approved_reimbursement_categories = (
                approved_reimbursement_categories_decisions.get(grant.id, [])
            )

            for reimbursement_category_id in approved_reimbursement_categories:
                if reimbursement_category_id not in reimbursement_categories:
                    continue

                reimbursement, created = GrantReimbursement.objects.update_or_create(
                    grant=grant,
                    category_id=reimbursement_category_id,
                    defaults={
                        "granted_amount": reimbursement_categories[
                            reimbursement_category_id
                        ].max_amount
                    },
                )

                if created:
                    create_addition_admin_log_entry(
                        request.user,
                        grant,
                        change_message=f"[Review Session] Reimbursement {reimbursement.category.name} added.",
                    )

        # Update internal notes in a separate pass.
        # This is intentionally separate from the main grant loop above because:
        # 1. Notes updates are independent of status/reimbursement changes
        # 2. A grant may have notes updated without any decision change
        # 3. Keeps the audit logging concerns (status changes) separate from notes
        if notes_updates:
            grants_to_update_notes = review_session.conference.grants.filter(
                id__in=notes_updates.keys()
            )
            for grant in grants_to_update_notes:
                new_notes = notes_updates.get(grant.id, "")
                if grant.internal_notes != new_notes:
                    grant.internal_notes = new_notes
                    grant.save(update_fields=["internal_notes"])

    def get_review_context(
        self,
        request: HttpRequest,
        review_session: ReviewSession,
        review_item_id: int,
        user_review: UserReview | None,
        admin_site: AdminSite,
    ) -> dict[str, Any]:
        """Return template context for reviewing a single grant."""
        private_comment = request.GET.get(
            "private_comment", user_review.private_comment if user_review else ""
        )
        comment = request.GET.get("comment", user_review.comment if user_review else "")

        grant = Grant.objects.get(id=review_item_id)
        previous_grants = Grant.objects.filter(
            user_id=grant.user_id,
            conference__organizer_id=grant.conference.organizer_id,
        ).exclude(conference_id=grant.conference_id)

        return dict(
            admin_site.each_context(request),
            grant=grant,
            has_sent_proposal=Submission.objects.non_cancelled()
            .filter(
                speaker_id=grant.user_id,
                conference_id=grant.conference_id,
            )
            .exists(),
            previous_grants=previous_grants,
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
            participant=Participant.objects.filter(
                user_id=grant.user_id,
                conference=grant.conference,
            ).first(),
        )

    def get_next_to_review_item_id(
        self,
        review_session: ReviewSession,
        user: User,
        skip_item: int | None = None,
        exclude: list[int] | None = None,  # noqa: ARG002 - unused, kept for interface consistency
        seen: list[int] | None = None,
    ) -> int | None:
        """Return the next grant ID to review, prioritising items with fewer votes."""
        seen = seen or []

        already_reviewed_ids = UserReview.objects.filter(
            user_id=user.id,
            review_session_id=review_session.id,
        ).values_list("grant_id", flat=True)

        items_to_exclude = (
            list(already_reviewed_ids) + ([skip_item] if skip_item else []) + seen
        )

        unvoted_item = (
            review_session.conference.grants.annotate(
                votes_received=Count(
                    "userreview",
                    filter=Q(userreview__review_session_id=review_session.id),
                )
            )
            .exclude(id__in=items_to_exclude)
            .order_by("votes_received", "?")
            .first()
        )

        return unvoted_item.id if unvoted_item else None

    def get_user_review_filter(self, review_item_id: int) -> dict[str, Any]:
        """Return filter kwargs for finding a user's grant review."""
        return {"grant_id": review_item_id}

    def get_user_review_create_values(self, review_item_id: int) -> dict[str, Any]:
        """Return values for creating a grant review."""
        return {"grant_id": review_item_id}


_PROPOSALS_ADAPTER = ProposalsReviewAdapter()
_GRANTS_ADAPTER = GrantsReviewAdapter()


def get_review_adapter(review_session: ReviewSession) -> ReviewAdapter:
    """Return the appropriate adapter for the given review session type."""
    if review_session.is_proposals_review:
        return _PROPOSALS_ADAPTER

    if review_session.is_grants_review:
        return _GRANTS_ADAPTER

    raise ValueError(f"Unknown review session type: {review_session.session_type}")
