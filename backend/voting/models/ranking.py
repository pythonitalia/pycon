from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField
from submissions.models import Submission


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

    def save(self, *args, **kwargs):
        super(RankRequest, self).save(*args, **kwargs)

        submissions = Submission.objects.filter(conference_id=self.conference.id)
        ranked_submissions = RankRequest.get_ranking(submissions)

        self.save_rank_submissions(ranked_submissions, submissions)

    @staticmethod
    def get_ranking(submissions):
        """Decide here how to rank submission (e,g. vote-engine)
        for "now" simply Sums votes.

        P. S. maybe we should make some *Strategy* in order to have all
        available and run different strategies...
        """

        from voting.models import Vote

        queryset = (
            Vote.objects.filter(submission__in=submissions)
            .values("submission_id", "submission__topic_id")
            .annotate(votes=Sum("value"))
            .order_by("-votes")
        )

        return queryset

    def save_rank_submissions(self, ranked_submissions, submissions):

        rank_obj = {}
        for index, rank in enumerate(ranked_submissions):
            rank_submission = RankSubmission(
                rank_request=self,
                submission=submissions.get(pk=rank["submission_id"]),
                absolute_rank=index + 1,
                absolute_score=rank["votes"],
            )
            rank_obj[rank["submission_id"]] = rank_submission

        import itertools

        def order_by(item):
            return item["submission__topic_id"]

        talk_rank_sub = sorted(ranked_submissions, key=order_by)
        for k, g in itertools.groupby(talk_rank_sub, order_by):
            for index, rank in enumerate(list(g)):
                rank_obj[rank["submission_id"]].topic_rank = index + 1
                rank_obj[rank["submission_id"]].topic_score = rank["votes"]
                rank_obj[rank["submission_id"]].save()


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
