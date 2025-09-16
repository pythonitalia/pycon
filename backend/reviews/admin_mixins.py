from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from reviews.models import ReviewSession, UserReview
from reviews.services import ReviewSessionService, ReviewItemService, ReviewVoteService


class ReviewSessionAdminMixin:
    """Mixin providing common review session admin functionality."""

    def get_review_session_service(
        self, review_session: ReviewSession
    ) -> ReviewSessionService:
        """Get a service instance for the review session."""
        return ReviewSessionService(review_session)

    def get_review_item_service(
        self, review_session: ReviewSession
    ) -> ReviewItemService:
        """Get an item service instance for the review session."""
        return ReviewItemService(review_session)

    def get_review_vote_service(
        self, review_session: ReviewSession
    ) -> ReviewVoteService:
        """Get a vote service instance for the review session."""
        return ReviewVoteService(review_session)

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


class ReviewSessionViewMixin:
    """Mixin providing review session view functionality."""

    def review_start_view(self, request, review_session_id):
        """Handle the review start view."""
        review_session = ReviewSession.objects.get(id=review_session_id)
        service = self.get_review_session_service(review_session)

        next_to_review = service.get_next_item_to_review(request.user)

        if not next_to_review:
            messages.warning(request, "No new proposal to review.")
            return redirect(
                reverse(
                    "admin:reviews-recap",
                    kwargs={"review_session_id": review_session_id},
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
        """Handle the review recap view."""
        review_session = ReviewSession.objects.get(id=review_session_id)
        service = self.get_review_session_service(review_session)

        if not service.can_user_review(request.user):
            raise PermissionDenied()

        if not service.can_see_recap_screen():
            messages.error(request, "You cannot see the recap of this session yet.")
            return redirect(
                reverse(
                    "admin:reviews_reviewsession_change",
                    kwargs={"object_id": review_session_id},
                )
            )

        if request.method == "POST":
            service.process_review_decisions(request)
            return redirect(
                reverse(
                    "admin:reviews-recap",
                    kwargs={"review_session_id": review_session_id},
                )
            )

        item_service = self.get_review_item_service(review_session)
        context = dict(
            self.admin_site.each_context(request),
            request=request,
            **service.get_recap_context_data(request),
        )

        template_name = item_service.get_recap_template_name()
        return TemplateResponse(request, template_name, context)

    def review_view(self, request, review_session_id, review_item_id):
        """Handle the individual review view."""
        review_session = ReviewSession.objects.get(id=review_session_id)
        service = self.get_review_session_service(review_session)

        if not service.can_user_review(request.user):
            raise PermissionDenied()

        if request.method == "GET":
            return self._handle_review_get_request(
                request, review_session, review_item_id
            )
        elif request.method == "POST":
            return self._handle_review_post_request(
                request, review_session, review_item_id
            )

    def _handle_review_get_request(self, request, review_session, review_item_id):
        """Handle GET request for review view."""
        # Get existing user review if any
        filter_options = {}
        if review_session.is_proposals_review:
            filter_options["proposal_id"] = review_item_id
        elif review_session.is_grants_review:
            filter_options["grant_id"] = review_item_id

        user_review = UserReview.objects.filter(
            user_id=request.user.id,
            review_session_id=review_session.id,
            **filter_options,
        ).first()

        item_service = self.get_review_item_service(review_session)
        context = dict(
            self.admin_site.each_context(request),
            **item_service.get_item_context_data(request, review_item_id, user_review),
        )

        template_name = item_service.get_review_template_name()
        return TemplateResponse(request, template_name, context)

    def _handle_review_post_request(self, request, review_session, review_item_id):
        """Handle POST request for review view."""
        from reviews.admin import SubmitVoteForm

        form = SubmitVoteForm(request.POST)
        form.is_valid()

        vote_service = self.get_review_vote_service(review_session)
        next_to_review = vote_service.process_vote_submission(
            request, review_item_id, form.cleaned_data
        )

        if next_to_review is None:
            # Error occurred, should have been handled by service
            return

        seen = [str(id_) for id_ in form.cleaned_data.get("seen", "").split(",") if id_]
        seen.append(str(review_item_id))
        exclude = form.cleaned_data.get("exclude", [])

        if not next_to_review:
            messages.warning(
                request, "No new items to review, showing an already seen one."
            )
            service = self.get_review_session_service(review_session)
            next_to_review = service.get_next_item_to_review(
                request.user, skip_item=review_item_id, exclude=exclude
            )

            if not next_to_review:
                messages.warning(request, "No new proposal to review.")
                return redirect(
                    reverse(
                        "admin:reviews-recap",
                        kwargs={"review_session_id": review_session.id},
                    )
                )

        return redirect(
            reverse(
                "admin:reviews-vote-view",
                kwargs={
                    "review_session_id": review_session.id,
                    "review_item_id": next_to_review,
                },
            )
            + f"?exclude={','.join(map(str, exclude))}&seen={','.join(seen)}"
        )
