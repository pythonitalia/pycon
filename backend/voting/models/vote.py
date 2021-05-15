from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel


class Vote(TimeStampedModel):
    VALUES = Choices(
        (1, "not_interested", _("Not Interested")),
        (2, "maybe", _("Maybe")),
        (3, "want_to_see", _("Want to See")),
        (4, "must_see", _("Must See")),
    )

    value = models.IntegerField(_("vote"), choices=VALUES)

    user_id = models.IntegerField(verbose_name=_("user"))

    submission = models.ForeignKey(
        "submissions.Submission",
        on_delete=models.CASCADE,
        verbose_name=_("submission"),
        related_name="votes",
    )

    def __str__(self):
        return f"{self.user_id} voted {self.value} for Submission {self.submission}"

    class Meta:
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")

        unique_together = ("user_id", "submission")
