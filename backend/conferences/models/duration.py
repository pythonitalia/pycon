from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Duration(models.Model):
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="durations",
    )

    name = models.CharField(_("name"), max_length=100)
    duration = models.PositiveIntegerField(
        _("duration"), validators=[MinValueValidator(1)]
    )
    notes = models.TextField(_("notes"), blank=True)
    allowed_submission_types = models.ManyToManyField(
        "submissions.SubmissionType", verbose_name=_("allowed submission types")
    )

    def __str__(self):
        return (
            f"{self.name} - {self.duration} mins (at Conference "
            f"{self.conference.name} <{self.conference.code}>)"
        )

    class Meta:
        verbose_name = _("Duration")
        verbose_name_plural = _("Durations")
