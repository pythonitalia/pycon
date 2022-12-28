from typing import List, Tuple, TypedDict

from django.db import models
from django.db.models import Count
from django.db.models.functions import Sqrt
from django.utils.translation import gettext_lazy as _
from model_utils.fields import AutoCreatedField

from conferences.models import Conference
from helpers.constants import GENDERS
from submissions.models import Submission, SubmissionTag
from users.client import get_users_data_by_ids


class RankStat(models.Model):
    class Type(models.TextChoices):
        SPEAKERS = "speakers", _("Speakers")
        SUBMISSIONS = "submissions", _("Submissions")
        GENDER = "gender", _("Gender")
        SUBMISSION_TYPE = "submission_type", _("Submission  Type")
        TOPIC = "topic", _("Topic")
        LANGUAGE = "language", _("Language")
        AUDIENCE_LEVEL = "audience_level", _("Audience Level")

    name = models.CharField(_("Name"), max_length=50)
    value = models.PositiveIntegerField(_("Value"))
    type = models.CharField(_("type"), choices=Type.choices, max_length=25)
    rank_request = models.ForeignKey(
        "voting.RankRequest",
        on_delete=models.CASCADE,
        verbose_name=_("Rank Request"),
        related_name="stats",
    )

    def __str__(self):
        return f"{self.type} ({self.name}) at <{self.rank_request.conference.code}> | {self.value}"


class Rank(TypedDict):
    submission_id: int
    submission__tag: SubmissionTag
    score: float


class RankRequest(models.Model):

    conference = models.OneToOneField(
        "conferences.Conference", on_delete=models.CASCADE, verbose_name=_("conference")
    )

    created = AutoCreatedField(_("created"))
    is_public = models.BooleanField(_("is_public"))

    def __str__(self):
        return (
            f"{self.conference.name} <{self.conference.code}>, "
            f"created on {self.created}"
        )

    def save(self, *args, **kwargs):
        super(RankRequest, self).save(*args, **kwargs)

        # do not recreate ranking
        if self.rank_submissions.exists():
            return

        ranked_submissions_by_tags = self.build_ranking(self.conference)

        self.save_rank_submissions(ranked_submissions_by_tags)
        self.build_stats()

    def build_ranking(self, conference: Conference):
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

    @staticmethod
    def users_most_voted_based(conference) -> List[Tuple[SubmissionTag, List[Rank]]]:
        """Builds the ranking based on the votes each user has gived
        This algorithm rewards users who have given more votes. If a user
        votes many submissions, it means that he cares about his choices so
        he must be rewarded by weighing his votes more.

        P. S. maybe we should make some *Strategy* in order to have all
        available and run different strategies...

        """

        from voting.models import Vote

        submissions = Submission.objects.filter(
            conference=conference, status=Submission.STATUS.proposed
        )

        tags = SubmissionTag.objects.filter(submission__in=submissions).distinct()

        votes = Vote.objects.filter(submission__conference=conference)

        users_weight = RankRequest.get_users_weights(votes)
        rankings = []
        for tag in tags:
            tag_submissions = submissions.filter(tags=tag)

            tag_ranking: List[Rank] = []
            for submission in tag_submissions:
                submission_votes = votes.filter(submission=submission)

                if submission_votes:
                    vote_info = {}
                    for vote in submission_votes:
                        vote_info[vote.id] = {
                            "normalised_vote": vote.value
                            * users_weight[(vote.user_id, tag.pk)],
                            "scale_factor": users_weight[(vote.user_id, tag.pk)],
                        }
                    score = sum(
                        [v["normalised_vote"] for v in vote_info.values()]
                    ) / sum([v["scale_factor"] for v in vote_info.values()])
                else:
                    score = 0

                rank: Rank = {
                    "submission_id": submission.id,
                    "submission__tag": tag,
                    "score": score,
                }
                tag_ranking.append(rank)
                tag_ranking = sorted(
                    tag_ranking, key=lambda k: k["score"], reverse=True
                )

            rankings.append((tag, tag_ranking))
        return rankings

    @staticmethod
    def get_users_weights(votes):
        queryset = votes.values("submission__tags", "user_id").annotate(
            weight=Sqrt(Count("submission__tags"))
        )
        return {
            (weight["user_id"], weight["submission__tags"]): weight["weight"]
            for weight in queryset
        }

    def save_rank_submissions(
        self, ranked_submissions_by_tag: List[Tuple[SubmissionTag, List[Rank]]]
    ):
        """Save the list of ranked submissions calculating the rank position
        from the score
        """

        for tag, submissions in ranked_submissions_by_tag:
            for index, rank in enumerate(submissions):
                RankSubmission.objects.create(
                    rank_request=self,
                    submission=Submission.objects.get(pk=rank["submission_id"]),
                    rank=index + 1,
                    score=rank["score"],
                    tag=tag,
                )

    def build_stats(self):
        submissions = self.rank_submissions.all()
        if not submissions:
            return

        # N. of submissions
        RankStat.objects.create(
            name="Submissions",
            type=RankStat.Type.SUBMISSIONS,
            value=submissions.count(),
            rank_request=self,
        )

        # N. of speakers
        distinct_speakers = (
            RankRequest.objects.filter(conference=self.conference)
            .values("rank_submissions__submission__speaker_id")
            .distinct()
        )
        RankStat.objects.create(
            name="Speakers",
            type=RankStat.Type.SPEAKERS,
            value=distinct_speakers.count(),
            rank_request=self,
        )

        # Gender
        speaker_ids = [
            i["rank_submissions__submission__speaker_id"] for i in distinct_speakers
        ]
        PREFETCHED_USERS_BY_ID = get_users_data_by_ids(list(speaker_ids))

        def filter_by_gender(user):
            return user["gender"] == key

        for key, value in GENDERS:
            count = len(list(filter(filter_by_gender, PREFETCHED_USERS_BY_ID.values())))

            RankStat.objects.create(
                name=f"{value}",
                type=RankStat.Type.GENDER,
                value=count,
                rank_request=self,
            )

        # N. submissions by SubmissionType
        for submission_type in self.conference.submission_types.all():
            count = submissions.filter(submission__type=submission_type).count()

            RankStat.objects.create(
                name=f"{submission_type.name}",
                type=RankStat.Type.SUBMISSION_TYPE,
                value=count,
                rank_request=self,
            )

        # N. submissions by Audience Level
        for audience_level in self.conference.audience_levels.all():
            count = submissions.filter(
                submission__audience_level=audience_level
            ).count()

            RankStat.objects.create(
                name=f"{audience_level.name}",
                type=RankStat.Type.AUDIENCE_LEVEL,
                value=count,
                rank_request=self,
            )

        # N. submissions by Language
        for language in self.conference.languages.all():
            count = submissions.filter(submission__languages=language).count()
            RankStat.objects.create(
                name=f"{language.name}",
                type=RankStat.Type.LANGUAGE,
                value=count,
                rank_request=self,
            )

        # N. submissions by Topic
        for topic in self.conference.topics.all():
            count = submissions.filter(submission__topic=topic).count()
            RankStat.objects.create(
                name=f"{topic.name}",
                type=RankStat.Type.TOPIC,
                value=count,
                rank_request=self,
            )


class RankSubmission(models.Model):

    rank_request = models.ForeignKey(
        RankRequest,
        on_delete=models.CASCADE,
        verbose_name=_("rank request"),
        related_name="rank_submissions",
    )

    tag = models.ForeignKey(
        "submissions.SubmissionTag",
        on_delete=models.CASCADE,
        verbose_name=_("tag"),
        null=True,
    )

    submission = models.ForeignKey(
        "submissions.Submission", on_delete=models.CASCADE, verbose_name=_("submission")
    )

    rank = models.PositiveIntegerField(_("rank"))
    score = models.DecimalField(_("score"), decimal_places=6, max_digits=9)

    def __str__(self):
        return (
            f"<{self.rank_request.conference.code}>"
            f" | {self.submission.title}"
            f" | {self.rank}"
        )
