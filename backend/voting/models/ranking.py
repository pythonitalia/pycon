import itertools

from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import Sqrt
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

        ranked_submissions = self.build_ranking(self.conference)

        self.save_rank_submissions(ranked_submissions)

    def build_ranking(self, conference):
        """Builds the ranking

        P. S. maybe we should make some *Strategy* in order to have all
        available and run different strategies...

        :return: list of dictionary ordered by score descending
        [{
            "submission_id": submission.id,
            "submission__topic_id": submission.topic_id,
            "score": score
        },
        ...
        ]
        """

        return RankRequest.users_most_voted_based(conference)
        # return RankRequest.simple_sum(conference)

    @staticmethod
    def users_most_voted_based(conference):
        """Builds the ranking based on the votes each user has gived
        This algorithm rewards users who have given more votes. If a user
        votes many submissions, it means that he cares about his choices so
        he must be rewarded by weighing his votes more.

        P. S. maybe we should make some *Strategy* in order to have all
        available and run different strategies...

        """

        from voting.models import Vote

        submissions = Submission.objects.filter(conference=conference)
        votes = Vote.objects.filter(submission__conference=conference)

        users_weight = RankRequest.get_users_weights(votes)

        ranking = []
        for submission in submissions:
            submission_votes = votes.filter(submission=submission)

            if submission_votes:
                vote_info = {}
                for vote in submission_votes:
                    vote_info[vote.id] = {
                        "normalised_vote": vote.value * users_weight[vote.user.id],
                        "scale_factor": users_weight[vote.user.id],
                    }
                score = sum([v["normalised_vote"] for v in vote_info.values()]) / sum(
                    [v["scale_factor"] for v in vote_info.values()]
                )
            else:
                score = 0
            rank = {
                "submission_id": submission.id,
                "submission__topic_id": submission.topic_id,
                "score": score,
            }
            ranking.append(rank)
        return sorted(ranking, key=lambda k: k["score"], reverse=True)

    @staticmethod
    def get_users_weights(votes):
        queryset = votes.values("user_id").annotate(weight=Sqrt(Count("submission_id")))
        return {weight["user_id"]: weight["weight"] for weight in queryset}

    @staticmethod
    def simple_sum(conference):
        """Simply sums the votes for each submission

        :param conference:
        """
        from voting.models import Vote

        submissions = Submission.objects.filter(conference=conference)
        ranking = (
            Vote.objects.filter(submission__in=submissions)
            .values("submission_id", "submission__topic_id")
            .annotate(score=Sum("value"))
            .order_by("-score")
        )
        return ranking

    def save_rank_submissions(self, scored_submissions):
        """Save the list of ranked submissions calculating the rank position
        from the score
        """

        ranked_obj = {}
        for index, rank in enumerate(scored_submissions):
            rank_submission = RankSubmission(
                rank_request=self,
                submission=Submission.objects.get(pk=rank["submission_id"]),
                absolute_rank=index + 1,
                absolute_score=rank["score"],
            )
            ranked_obj[rank["submission_id"]] = rank_submission

        # group by topic to generate the relative ranking
        def group_by(item):
            return item["submission__topic_id"]

        scored_submissions = sorted(scored_submissions, key=group_by)

        for k, g in itertools.groupby(scored_submissions, group_by):
            for index, rank in enumerate(list(g)):
                ranked_obj[rank["submission_id"]].topic_rank = index + 1
                ranked_obj[rank["submission_id"]].save()


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
    absolute_score = models.DecimalField(
        _("absolute score"), decimal_places=6, max_digits=9
    )
    topic_rank = models.PositiveIntegerField(_("topic rank"))

    def __str__(self):
        return (
            f"<{self.rank_request.conference.code}>"
            f" | {self.submission.title}"
            f" | {self.absolute_rank}"
        )
