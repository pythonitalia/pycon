from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField


class RankRequest(models.Model):

    conference = models.ForeignKey(
        "conferences.Conference", on_delete=models.CASCADE, verbose_name=_("conference")
    )

    created = AutoCreatedField(_("created"))

    def __str__(self):
        return (
            f"{self.conference.name} <{self.conference.code}>, "
            f"created on {self.created}"
        )


class RankSubmission(models.Model):

    rank_request = models.ForeignKey(
        RankRequest,
        on_delete=models.CASCADE,
        verbose_name=_("rank request"),
        related_name="rank_submissions",
    )

    submission = models.ForeignKey(
        "submissions.Submission", on_delete=models.CASCADE, verbose_name=_("submission")
    )

    absolute_rank = models.PositiveIntegerField(_("absolute rank"))

    absolute_score = models.PositiveIntegerField(_("absolute score"))

    topic_rank = models.PositiveIntegerField(_("topic rank"))

    topic_score = models.PositiveIntegerField(_("topic score"))

    def __str__(self):
        return (
            f"<{self.rank_request.conference.code}>"
            f" | {self.submission.title}"
            f" | {self.absolute_rank}"
        )
