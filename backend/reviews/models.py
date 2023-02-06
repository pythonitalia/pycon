from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel

from conferences.models.conference import Conference


class ReviewSession(TimeStampedModel):
    class SessionType(models.TextChoices):
        PROPOSALS = "proposals", _("Proposals")
        GRANTS = "grants", _("Grants")

    session_type = models.CharField(
        max_length=100,
        choices=SessionType.choices,
    )
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    @property
    def is_proposals_review(self):
        return self.session_type == self.SessionType.PROPOSALS

    @property
    def is_grants_review(self):
        return self.session_type == self.SessionType.GRANTS


class AvailableScoreOption(TimeStampedModel, OrderedModel):
    review_session = models.ForeignKey(ReviewSession, on_delete=models.CASCADE)

    numeric_value = models.IntegerField()
    label = models.CharField(max_length=100)

    class Meta:
        unique_together = ("review_session", "numeric_value")


class UserReview(TimeStampedModel):
    review_session = models.ForeignKey(ReviewSession, on_delete=models.CASCADE)
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
