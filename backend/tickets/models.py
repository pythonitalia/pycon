from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


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

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = _('Ticket Question')
        verbose_name_plural = _('Ticket Questions')


class TicketQuestionChoices(TimeStampedModel):
    question = models.ForeignKey(
        TicketQuestion,
        on_delete=models.PROTECT,
        verbose_name=_('question')
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

    answer = models.ForeignKey(
        'tickets.TicketQuestionChoices',
        on_delete=models.PROTECT,
        verbose_name=_('answer'),
        null=True
    )
