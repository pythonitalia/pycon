from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class IncludedEvent(TimeStampedModel):
    """
    An included event is a pretix event that should be considerated
    when checking if the user can vote for the conference or not
    """

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        related_name="included_voting_events",
        verbose_name=_("conference"),
    )
    pretix_organizer_id = models.CharField(
        _("pretix organizer id"), max_length=200, blank=False
    )
    pretix_event_id = models.CharField(
        _("pretix event id"), max_length=200, blank=False
    )

    class Meta:
        verbose_name = _("included event for voting")
        verbose_name_plural = _("included events for voting")
