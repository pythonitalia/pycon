from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from tickets import QUESTION_TYPE_CHOICE, QUESTION_TYPES


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

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


class TicketQuestion(TimeStampedModel):
    text = models.CharField(_("text"), max_length=256)
    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default=QUESTION_TYPE_CHOICE,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _("Ticket Question")
        verbose_name_plural = _("Ticket Questions")


class TicketQuestionChoice(TimeStampedModel):
    question = models.ForeignKey(
        TicketQuestion,
        on_delete=models.PROTECT,
        related_name="choices",
        verbose_name=_("question"),
    )

    choice = models.CharField(_("text"), max_length=256)

    class Meta:
        verbose_name = _("Ticket question choice")
        verbose_name_plural = _("Ticket question choices")


class UserAnswer(TimeStampedModel):
    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.PROTECT,
        verbose_name=_("ticket"),
        related_name="answers",
    )

    # TODO: Replace with TicketFareQuestion?
    question = models.ForeignKey(
        "tickets.TicketQuestion",
        on_delete=models.PROTECT,
        verbose_name=_("question"),
        related_name="questions",
    )

    answer = models.CharField(_("answer"), max_length=256, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self.question_id and self.question.question_type == QUESTION_TYPE_CHOICE:
            if self.answer not in self.question.choices.all().values_list(
                "choice", flat=True
            ):
                raise ValidationError(
                    {"answer": _("Answer not possible for this question.")}
                )

    class Meta:
        verbose_name = _("User answer")
        verbose_name_plural = _("User answers")
        unique_together = ("ticket", "question")
