from django.conf import settings
from django.core import exceptions
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class VoteRange(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    first = models.IntegerField(_('first'))
    last = models.IntegerField(_('last'))
    step = models.FloatField(_('step'), validators=[MinValueValidator(0.1)])

    def clean(self):
        super().clean()

        if self.first > self.last:
            raise exceptions.ValidationError(
                _('First vote cannot be greater then the last'))

        if self.step < 0:
            raise exceptions.ValidationError(
                _('Step cannot be less than zero'))

    def __str__(self):
        return f'{self.name} goes from {self.first} to {self.last} with step {self.step}'


class Vote(TimeStampedModel):
    value = models.FloatField(_('vote'))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        on_delete=models.PROTECT,
    )

    submission = models.ForeignKey(
        'submissions.Submission',
        on_delete=models.CASCADE,
        verbose_name=_('submission'),
        related_name='votes'
    )

    def clean(self):
        super().clean()
        if not self.submission.conference.vote_range.first <= self.value <= \
               self.submission.conference.vote_range.last:
            raise exceptions.ValidationError(_(
                f'Vote must be a value between '
                f'{self.submission.conference.vote_range.first} and '
                f'{self.submission.conference.vote_range.last}'))

    def __str__(self):
        return f'{self.user} voted {self.value} for Submission {self.submission}'

    def save(self, *args, **kwargs):
        """Updates the instance if already exist a User's vote for the same
        submission
        """
        try:
            _vote = Vote.objects.get(user=self.user,
                                     submission=self.submission)
            self.id = _vote.id
            super().save(force_update=True, *args, **kwargs)
        except Vote.DoesNotExist:
            super().save(*args, **kwargs)
