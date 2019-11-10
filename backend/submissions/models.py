from django.conf import settings
from django.core import exceptions
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
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
    slug = models.SlugField(_("slug"), max_length=200)
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

    audience_level = models.ForeignKey(
        "conferences.AudienceLevel",
        verbose_name=_("audience level"),
        on_delete=models.PROTECT,
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
                {"duration": _(f"{str(self.duration)} is not an allowed duration type")}
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
                        f"the submission type {str(self.type)}"
                    )
                }
            )

        if (
            self.audience_level_id
            and not self.conference.audience_levels.filter(
                id=self.audience_level_id
            ).exists()
        ):
            raise exceptions.ValidationError(
                {
                    "audience_level": _(
                        "%(audience_level)s is not an allowed audience level"
                    )
                    % {"audience_level": str(self.audience_level)}
                }
            )

    def get_admin_url(self):
        return reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=(self.pk,),
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at Conference {self.conference_id}"


class SubmissionType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
