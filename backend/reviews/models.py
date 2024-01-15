from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel

from conferences.models.conference import Conference


class ReviewSession(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        REVIEWING = "reviewing", _("Reviewing")
        COMPLETED = "completed", _("Completed")

    class SessionType(models.TextChoices):
        PROPOSALS = "proposals", _("Proposals")
        GRANTS = "grants", _("Grants")

    session_type = models.CharField(
        max_length=100,
        choices=SessionType.choices,
    )
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    def __str__(self) -> str:
        return f"{self.conference.name} - {self.session_type}"

    @property
    def is_draft(self):
        return self.status == self.Status.DRAFT

    @property
    def is_reviewing(self):
        return self.status == self.Status.REVIEWING

    @property
    def is_completed(self):
        return self.status == self.Status.COMPLETED

    @property
    def is_proposals_review(self):
        return self.session_type == self.SessionType.PROPOSALS

    @property
    def is_grants_review(self):
        return self.session_type == self.SessionType.GRANTS

    @property
    def has_user_reviews(self):
        return self.user_reviews.exists()

    @property
    def can_see_recap_screen(self):
        if self.is_proposals_review:
            return True

        if self.is_grants_review and self.is_completed:
            return True

        return False

    @property
    def can_review_items(self):
        if self.is_proposals_review:
            return True

        if self.is_grants_review and self.is_reviewing:
            return True

        return False

    def user_can_review(self, user):
        if self.is_proposals_review:
            return user.has_perms(
                ["reviews.review_reviewsession", "submissions.view_submission"], self
            )

        if self.is_grants_review:
            return user.has_perms(
                ["reviews.review_reviewsession", "grants.view_grant"], self
            )

        return False

    class Meta:
        permissions = [
            ("review_reviewsession", "Can review items"),
            ("decision_reviewsession", "Can make decisions on items"),
        ]


class AvailableScoreOption(TimeStampedModel, OrderedModel):
    review_session = models.ForeignKey(ReviewSession, on_delete=models.CASCADE)

    numeric_value = models.IntegerField()
    label = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.numeric_value} - {self.label}"

    class Meta:
        unique_together = ("review_session", "numeric_value")


class UserReview(TimeStampedModel):
    review_session = models.ForeignKey(
        ReviewSession, on_delete=models.CASCADE, related_name="user_reviews"
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
    )
    proposal = models.ForeignKey(
        "submissions.Submission",
        on_delete=models.CASCADE,
        null=True,
    )
    grant = models.ForeignKey(
        "grants.Grant",
        on_delete=models.CASCADE,
        null=True,
    )
    score = models.ForeignKey(AvailableScoreOption, on_delete=models.PROTECT)
    comment = models.TextField(blank=True)
    private_comment = models.TextField(blank=True)

    @property
    def object_id(self):
        return self.proposal_id or self.grant_id
