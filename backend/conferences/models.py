from django.db import models

from django.utils import timezone
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeFramedModel, TimeStampedModel


class Conference(TimeStampedModel, TimeFramedModel):
    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=10, unique=True)
    slug = models.SlugField()

    # deadlines
    cfp_start = models.DateTimeField(_('call for proposals starts at'), blank=True, null=True)
    cfp_end = models.DateTimeField(_('call for proposals ends at'), blank=True, null=True)

    voting_start = models.DateTimeField(_('voting starts at'), blank=True, null=True)
    voting_end = models.DateTimeField(_('voting ends at'), blank=True, null=True)

    refund_start = models.DateTimeField(_('refund starts at'), blank=True, null=True)
    refund_end = models.DateTimeField(_('refund ends at'), blank=True, null=True)

    def clean(self):
        # Specify a date range as a pair: (start, end, what)
        date_ranges = [
            (self.start, self.end, _('Conference')),
            (self.cfp_start, self.cfp_end, _('CFP')),
            (self.voting_start, self.voting_end, _('Voting')),
            (self.refund_start, self.refund_end, _('Refund')),
        ]

        for date_range in date_ranges:
            start, end, what = date_range

            if start and not end or not start and end:
                raise exceptions.ValidationError(f"{_('Please specify both start and end for')} {what}")

            if not start or not end:
                continue

            if start > end:
                raise exceptions.ValidationError(f"{what} {_('start date cannot be after end')}")

    @property
    def is_voting_open(self):
        if not self.voting_start:
            return False

        today = timezone.now()
        return self.voting_start <= today <= self.voting_end

    @property
    def is_cfp_open(self):
        if not self.cfp_start:
            return False

        today = timezone.now()
        return self.cfp_start <= today <= self.cfp_end

    @property
    def can_user_refund(self):
        if not self.refund_start:
            return False

        today = timezone.now()
        return self.refund_start <= today <= self.refund_end

    def __str__(self):
        return f'{self.name} <{self.slug}>'

    class Meta:
        verbose_name = _('Conference')
        verbose_name_plural = _('Conferences')
