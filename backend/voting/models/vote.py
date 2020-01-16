from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
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

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.PROTECT
    )

    submission = models.ForeignKey(
        "submissions.Submission",
        on_delete=models.CASCADE,
        verbose_name=_("submission"),
        related_name="votes",
    )

    def __str__(self):
        return f"{self.user} voted {self.value} for Submission {self.submission}"

    class Meta:
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")

        unique_together = ("user", "submission")
