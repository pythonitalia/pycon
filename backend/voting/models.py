from django.conf import settings
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from model_utils import Choices


class Vote(TimeStampedModel):
    VALUES = Choices(
        (0, 'not_interested', _('Not Interested')),
        (1, 'maybe', _('Maybe')),
        (2, 'want_to_see', _('Want to See')),
        (3, 'must_see', _('Must See')),
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

    def save(self, *args, **kwargs):
        """Updates the instance if already exist a User's vote for the same
        submission
        """
        try:
            _vote = Vote.objects.get(user=self.user, submission=self.submission)
            self.id = _vote.id
            super().save(force_update=True, *args, **kwargs)
        except Vote.DoesNotExist:
            super().save(*args, **kwargs)
