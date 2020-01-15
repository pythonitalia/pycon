from conferences.models import Conference
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum
from submissions.models import Submission
from voting.models import Vote


class Command(BaseCommand):
    help = "Generates the Submission Ranking from users' votes"

    def add_arguments(self, parser):
        parser.add_argument("conference", type=str, help="The Conference code")

    def print_counts(self, submissions):
        submissions_votes = Vote.objects.filter(submission__in=submissions).values(
            "user"
        )
        votes = submissions_votes.count()
        users = submissions_votes.distinct().count()
        self.stdout.write(
            f"{submissions.count()} talks | {users} users | {votes} votes"
        )

    def rank_submissions(self, submissions):
        """Decide here how to rank submission (e,g. vote-engine)
        for "now" simply Sums votes.

        P. S. maybe we should make some *Strategy* in order to have all
        available and run different strategies...

        :param submissions: Submission queryset
        :return: submissions sorted by ranking in descending order
        :rtype: list of dictionary

        Example of return:
            [
                {
                    "submission_id": <pk>,
                    "votes": N,
                    "submission": Submission object
                 },
                 ...
             ]
        """

        queryset = (
            Vote.objects.filter(submission__in=submissions)
            .values("submission_id")
            .annotate(votes=Sum("value"))
            .order_by("-votes")
        )
        # list(submissions)[0].votes.all().aggregate(total=Sum("value"))
        return [
            {"submission": submissions.get(pk=i["submission_id"]), **i}
            for i in queryset
        ]

    def print_ranking(self, ranking):
        for rank in ranking:
            submission = rank["submission"]
            votes = rank["votes"]
            langs = [l.code for l in submission.languages.all()]
            msg = " | ".join(
                [
                    str(submission.pk),
                    str(votes),
                    submission.type.name,
                    str(submission.duration.duration),
                    submission.title,
                    submission.topic.name,
                    " ".join(langs),
                    submission.speaker.full_name,
                    submission.speaker.gender,
                ]
            )
            self.stdout.write(msg)

    def handle(self, *args, **options):
        self.stdout.write("Starting...")

        try:
            conference = Conference.objects.get(code=options["conference"])
        except Conference.DoesNotExist:
            raise CommandError(f'Conference "{options["conference"]}" does not exist')

        submissions = Submission.objects.filter(conference_id=conference.id)

        self.print_counts(submissions)
        ranking = self.rank_submissions(submissions)
        self.print_ranking(ranking)
