from django.conf import settings
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Submission(TimeStampedModel):
    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="submissions",
    )

    title = models.CharField(_("title"), max_length=100)
    abstract = models.TextField(_("abstract"), max_length=1000)
    elevator_pitch = models.TextField(
        _("elevator pitch"), max_length=300, default="", blank=True
    )
    notes = models.TextField(_("notes"), default="", blank=True)

    speaker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("speaker"),
        on_delete=models.PROTECT,
        related_name="submissions",
    )

    topic = models.ForeignKey(
        "conferences.Topic", verbose_name=_("topic"), on_delete=models.PROTECT
    )

    language = models.ForeignKey(
        "languages.Language", verbose_name=_("language"), on_delete=models.PROTECT
    )

    type = models.ForeignKey(
        "submissions.SubmissionType", verbose_name=_("type"), on_delete=models.PROTECT
    )

    duration = models.ForeignKey(
        "conferences.Duration", verbose_name=_("duration"), on_delete=models.PROTECT
    )

    def clean(self):
        if (
            self.topic_id
            and not self.conference.topics.filter(id=self.topic_id).exists()
        ):
            raise exceptions.ValidationError(
                {
                    "topic": _("%(topic)s is not a valid topic")
                    % {"topic": str(self.topic)}
                }
            )

        if (
            self.language_id
            and not self.conference.languages.filter(id=self.language_id).exists()
        ):
            raise exceptions.ValidationError(
                {
                    "language": _("%(language)s is not an allowed language")
                    % {"language": str(self.language)}
                }
            )

        if (
            self.type_id
            and not self.conference.submission_types.filter(id=self.type_id).exists()
        ):
            raise exceptions.ValidationError(
                {
                    "type": _("%(submission_type)s is not an allowed submission type")
                    % {"submission_type": str(self.type)}
                }
            )

        if (
            self.duration_id
            and not self.conference.durations.filter(id=self.duration_id).exists()
        ):
            raise exceptions.ValidationError(
                {
                    "duration": _("%(duration)s is not an allowed duration type")
                    % {"duration": str(self.duration)}
                }
            )

        if (
            self.duration_id
            and self.type_id
            and not self.duration.allowed_submission_types.filter(
                id=self.type_id
            ).exists()
        ):

            raise exceptions.ValidationError(
                {
                    "duration": _(
                        f"Duration {str(self.duration)} is not an allowed for "
                        "the submission type {str(self.type)}"
                    )
                }
            )

    def __str__(self):
        return f"{self.title} at Conference {self.conference_id}"


class SubmissionType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
