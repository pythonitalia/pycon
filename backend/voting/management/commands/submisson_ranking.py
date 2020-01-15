from conferences.models import Conference
from django.core.management.base import BaseCommand, CommandError
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

    def ranking_submissions(self, submissions):
        pass

    def handle(self, *args, **options):
        self.stdout.write("Starting...")

        try:
            conference = Conference.objects.get(code=options["conference"])
        except Conference.DoesNotExist:
            raise CommandError(f'Conference "{options["conference"]}" does not exist')

        submissions = Submission.objects.filter(conference=conference)

        self.print_counts(submissions)
        self.ranking_submissions(submissions)
