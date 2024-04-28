from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class Vote(TimeStampedModel):
    class Values(models.IntegerChoices):
        not_interested = 1, _("Not Interested")
        maybe = 2, _("Maybe")
        want_to_see = 3, _("Want to See")
        must_see = 4, _("Must See")

    value = models.IntegerField(_("vote"), choices=Values.choices)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("user"),
        related_name="+",
    )

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

        unique_together = ("user", "submission")
