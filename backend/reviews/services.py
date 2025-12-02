from typing import Any, Dict, List, Optional, TYPE_CHECKING
import urllib.parse

from django.contrib import messages
from django.db import models
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from reviews.models import AvailableScoreOption, ReviewSession, UserReview
from reviews.strategies import ReviewStrategyFactory

if TYPE_CHECKING:
    from users.models import User


class ReviewSessionService:
    """Service class for managing review sessions and workflows."""

    def __init__(self, review_session: ReviewSession):
        self.review_session = review_session
        self.strategy = ReviewStrategyFactory.get_strategy(review_session.session_type)

    def can_user_review(self, user: "User") -> bool:
        """Check if a user can review items in this session."""
        return self.review_session.user_can_review(user)

    def can_review_items(self) -> bool:
        """Check if items can be reviewed in this session."""
        return self.review_session.can_review_items

    def can_see_recap_screen(self) -> bool:
        """Check if the recap screen can be viewed for this session."""
        return self.review_session.can_see_recap_screen

    def get_next_item_to_review(
        self,
        user: "User",
        skip_item: Optional[int] = None,
        exclude: Optional[List[int]] = None,
        seen: Optional[List[int]] = None,
    ) -> Optional[int]:
        """Get the next item ID to review for the given user."""
        return self.strategy.get_next_item_to_review(
            self.review_session, user, skip_item, exclude, seen
        )

    def process_review_decisions(self, request: HttpRequest) -> None:
        """Process decisions made during the review recap phase."""
        self.strategy.process_review_decisions(request, self.review_session)

    def get_recap_context_data(self, request: HttpRequest) -> Dict[str, Any]:
        """Get context data for the recap view."""
        base_context = {
            "review_session_id": self.review_session.id,
            "review_session_repr": str(self.review_session),
            "review_session": self.review_session,
            "title": "Recap",
        }
        strategy_context = self.strategy.get_recap_context_data(
            request, self.review_session
        )
        return {**base_context, **strategy_context}


class ReviewItemService:
    """Service class for handling individual review items."""

    def __init__(self, review_session: ReviewSession):
        self.review_session = review_session
        self.strategy = ReviewStrategyFactory.get_strategy(review_session.session_type)

    def get_review_template_name(self) -> str:
        """Get the template name for reviewing items."""
        return self.strategy.get_review_template_name()

    def get_recap_template_name(self) -> str:
        """Get the template name for the recap view."""
        return self.strategy.get_recap_template_name()

    def get_item_context_data(
        self,
        request: HttpRequest,
        review_item_id: int,
        user_review: Optional[UserReview] = None,
    ) -> Dict[str, Any]:
        """Get context data for reviewing a specific item."""

        private_comment = request.GET.get(
            "private_comment", user_review.private_comment if user_review else ""
        )
        comment = request.GET.get("comment", user_review.comment if user_review else "")

        base_context = {
            "available_scores": AvailableScoreOption.objects.filter(
                review_session_id=self.review_session.id
            ).order_by("-numeric_value"),
            "review_session_id": self.review_session.id,
            "user_review": user_review,
            "private_comment": private_comment,
            "comment": comment,
            "review_session_repr": str(self.review_session),
            "can_review_items": self.review_session.can_review_items,
            "seen": request.GET.get("seen", "").split(","),
        }

        # Add item-specific context based on review type
        if self.review_session.is_proposals_review:
            base_context.update(
                self._get_proposal_context_data(request, review_item_id)
            )
        elif self.review_session.is_grants_review:
            base_context.update(self._get_grant_context_data(request, review_item_id))

        return base_context

    def _get_proposal_context_data(
        self, request: HttpRequest, review_item_id: int
    ) -> Dict[str, Any]:
        """Get context data specific to proposal reviews."""
        from submissions.models import Submission, SubmissionTag
        from grants.models import Grant
        from participants.models import Participant

        proposal = (
            Submission.objects.for_conference(self.review_session.conference_id)
            .prefetch_related(
                "rankings",
                "rankings__tag",
                models.Prefetch(
                    "userreview_set",
                    queryset=UserReview.objects.prefetch_related(
                        "user", "score"
                    ).filter(review_session_id=self.review_session.id),
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

        tags_to_filter = (
            SubmissionTag.objects.filter(id__in=used_tags).order_by("name").all()
        )

        return {
            "proposal": proposal,
            "languages": proposal.languages.all(),
            "proposal_id": review_item_id,
            "has_italian_language": any(
                language for language in languages if language.code == "it"
            ),
            "has_english_language": any(
                language for language in languages if language.code == "en"
            ),
            "speaker": speaker,
            "grant": grant,
            "grant_link": grant_link,
            "participant": Participant.objects.filter(
                user_id=proposal.speaker_id,
                conference=proposal.conference,
            ).first(),
            "tags_to_filter": tags_to_filter,
            "tags_already_excluded": tags_already_excluded,
            "existing_comment": existing_comment,
            "title": f"Proposal Review: {proposal.title.localize('en')}",
        }

    def _get_grant_context_data(
        self, request: HttpRequest, review_item_id: int
    ) -> Dict[str, Any]:
        """Get context data specific to grant reviews."""
        from grants.models import Grant
        from submissions.models import Submission
        from participants.models import Participant

        grant = Grant.objects.get(id=review_item_id)
        previous_grants = Grant.objects.filter(
            user_id=grant.user_id,
            conference__organizer_id=grant.conference.organizer_id,
        ).exclude(conference_id=grant.conference_id)

        return {
            "grant": grant,
            "has_sent_proposal": Submission.objects.non_cancelled()
            .filter(
                speaker_id=grant.user_id,
                conference_id=grant.conference_id,
            )
            .exists(),
            "previous_grants": previous_grants,
            "title": f"Grant Review: {grant.user.display_name}",
            "participant": Participant.objects.filter(
                user_id=grant.user_id,
                conference=grant.conference,
            ).first(),
        }


class ReviewVoteService:
    """Service class for handling voting logic."""

    def __init__(self, review_session: ReviewSession):
        self.review_session = review_session
        self.strategy = ReviewStrategyFactory.get_strategy(review_session.session_type)

    def process_vote_submission(
        self, request: HttpRequest, review_item_id: int, form_data: Dict[str, Any]
    ) -> Optional[int]:
        """Process a vote submission and return the next item ID to review."""
        seen = [str(id_) for id_ in form_data.get("seen", "").split(",") if id_]
        seen.append(str(review_item_id))

        exclude = form_data.get("exclude", [])

        if form_data.get("_skip"):
            # Skipping to the next item without voting
            return self._get_next_item(request.user, review_item_id, exclude, seen)
        elif form_data.get("_next"):
            if not self.strategy.validate_user_review_data(form_data):
                self._handle_invalid_vote(
                    request, review_item_id, form_data, exclude, seen
                )
                return None

            self._save_user_review(request.user, review_item_id, form_data)
            return self._get_next_item(request.user, None, exclude, seen)

        return None

    def _get_next_item(
        self,
        user: "User",
        skip_item: Optional[int] = None,
        exclude: Optional[List[int]] = None,
        seen: Optional[List[int]] = None,
    ) -> Optional[int]:
        """Get the next item to review."""
        next_to_review = self.strategy.get_next_item_to_review(
            self.review_session, user, skip_item, exclude, seen
        )

        if not next_to_review:
            # Try again without excluding seen items
            next_to_review = self.strategy.get_next_item_to_review(
                self.review_session, user, skip_item, exclude
            )

        return next_to_review

    def _save_user_review(
        self, user: "User", review_item_id: int, form_data: Dict[str, Any]
    ) -> None:
        """Save or update a user review."""
        values = {
            "user_id": user.id,
            "review_session_id": self.review_session.id,
        }

        # Add item-specific fields
        item_fields = self.strategy.create_user_review_fields(review_item_id)
        values.update(item_fields)

        UserReview.objects.update_or_create(
            **values,
            defaults={
                "score_id": form_data["score"].id,
                "comment": form_data.get("comment", ""),
                "private_comment": form_data.get("private_comment", ""),
            },
        )

    def _handle_invalid_vote(
        self,
        request: HttpRequest,
        review_item_id: int,
        form_data: Dict[str, Any],
        exclude: List[int],
        seen: List[int],
    ) -> None:
        """Handle invalid vote submission by redirecting with error message."""
        messages.error(request, "Invalid vote")
        comment = urllib.parse.quote(form_data.get("comment", ""))
        private_comment = urllib.parse.quote(form_data.get("private_comment", ""))

        redirect_url = (
            reverse(
                "admin:reviews-vote-view",
                kwargs={
                    "review_session_id": self.review_session.id,
                    "review_item_id": review_item_id,
                },
            )
            + f"?exclude={','.join(map(str, exclude))}"
            + f"&seen={','.join(seen)}"
            + f"&comment={comment}"
            + f"&private_comment={private_comment}"
        )
        raise redirect(redirect_url)
