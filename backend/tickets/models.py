from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from tickets import QUESTION_TYPES, QUESTION_TYPE_CHOICE


class Ticket(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_("user"),
        related_name="tickets",
    )

    ticket_fare = models.ForeignKey(
        "conferences.TicketFare",
        on_delete=models.PROTECT,
        verbose_name=_("ticket fare"),
    )

    order = models.ForeignKey(
        "orders.Order", on_delete=models.PROTECT, verbose_name=_("order")
    )


class TicketQuestion(TimeStampedModel):
    text = models.CharField(_('text'), max_length=256)
    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default=QUESTION_TYPE_CHOICE,
        blank=False, null=False,
    )

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = _('Ticket Question')
        verbose_name_plural = _('Ticket Questions')


class TicketQuestionChoices(TimeStampedModel):
    question = models.ForeignKey(
        TicketQuestion,
        on_delete=models.PROTECT,
        related_name='choices',
        verbose_name=_('question'),
    )

    choice = models.CharField(_('text'), max_length=256)


class UserAnswer(TimeStampedModel):
    ticket = models.ForeignKey(
        'tickets.Ticket',
        on_delete=models.PROTECT,
        verbose_name=_('ticket'),
        related_name='answers'
    )

    question = models.ForeignKey(
        'tickets.TicketQuestion',
        on_delete=models.PROTECT,
        verbose_name=_('ticket'),
        related_name='questions'
    )

    answer = models.CharField(
        max_length=256,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(UserAnswer, self).save(*args, **kwargs)

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.question.question_type == QUESTION_TYPE_CHOICE:
            if self.answer not in self.question.choices.all().values_list('choice', flat=True):
                raise ValidationError({'answer': _('Answer not possible for this question.')})
