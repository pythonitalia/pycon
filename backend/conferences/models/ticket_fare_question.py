from django.db import models
from django.utils.translation import ugettext_lazy as _


class TicketFareQuestion(models.Model):
    ticket_fare = models.ForeignKey(
        "conferences.TicketFare",
        on_delete=models.CASCADE,
        verbose_name=_("ticket fare"),
        related_name="questions",
    )

    question = models.ForeignKey(
        "tickets.TicketQuestion", on_delete=models.CASCADE, verbose_name=_("question")
    )

    is_required = models.BooleanField(_("required"), default=False)

    class Meta:
        verbose_name = _("Ticket fare question")
        verbose_name_plural = _("Ticket fare questions")
        unique_together = ("ticket_fare", "question")
