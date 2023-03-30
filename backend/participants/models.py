from django.db import models
from django.utils.translation import gettext_lazy as _


class Participant(models.Model):
    class SpeakerLevels(models.TextChoices):
        new = "new", _("New speaker")
        intermediate = "intermediate", _("Intermediate experience")
        experienced = "experienced", _("Experienced")

    conference = models.ForeignKey(
        "conferences.Conference",
        on_delete=models.CASCADE,
        verbose_name=_("conference"),
        related_name="participants",
    )
    user_id = models.IntegerField(verbose_name=_("user_id"))

    photo = models.TextField(_("photo"))
    bio = models.TextField(max_length=2048)
    website = models.URLField(max_length=2048, blank=True)
    twitter_handle = models.CharField(max_length=15, blank=True)
    instagram_handle = models.CharField(max_length=30, blank=True)
    linkedin_url = models.CharField(max_length=2048, blank=True)
    facebook_url = models.CharField(max_length=2048, blank=True)
    mastodon_handle = models.CharField(max_length=2048, blank=True)

    speaker_level = models.CharField(
        _("speaker level"), choices=SpeakerLevels.choices, max_length=20
    )
    previous_talk_video = models.URLField(
        _("previous talk video"), blank=True, max_length=2049
    )

    def __str__(self) -> str:
        return f"Participant {self.user_id} for {self.conference}"

    class Meta:
        unique_together = ("conference", "user_id")
