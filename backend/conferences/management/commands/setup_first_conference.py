from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from conferences.models import (
    AudienceLevel,
    Conference,
    Deadline,
    Duration,
    Topic,
)
from i18n.strings import LazyI18nString
from languages.models import Language
from organizers.models import Organizer
from sponsors.models import Sponsor, SponsorLevel
from submissions.models import (
    Submission,
    SubmissionTag,
    SubmissionType,
)
from users.models import User


CODE = "demo-conf"

TOPICS = ["Web", "Data Science", "DevOps", "AI"]
AUDIENCE_LEVELS = ["Beginner", "Intermediate", "Advanced"]
SUBMISSION_TYPES = ["talk", "tutorial"]
TAG_NAMES = ["python", "web", "data", "testing", "devops"]

SPEAKERS = [
    ("alice@example.com", "Alice Rossi"),
    ("bob@example.com", "Bob Bianchi"),
    ("clara@example.com", "Clara Verdi"),
]

TALKS = [
    ("Async Python: Beyond the Basics", "talk", 45),
    ("Type Hints in Practice", "talk", 30),
    ("Hands-on Django Workshop", "tutorial", 180),
    ("Building APIs with FastAPI", "talk", 45),
    ("Testing Strategies", "talk", 30),
]

SPONSOR_LEVELS = [
    ("Keystone", 10000, "blue"),
    ("Gold", 7000, "yellow"),
    ("Silver", 5000, "gray"),
]

SPONSORS = [
    ("Snakely", "https://snakely.example", "Keystone"),
    ("JavaPanda", "https://javapanda.example", "Gold"),
    ("PyForge", "https://pyforge.example", "Silver"),
]


class Command(BaseCommand):
    help = "Set up the first Conference with dummy data for local development"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Recreate the demo conference even if one already exists",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["force"]:
            existing = Conference.objects.filter(code=CODE).first()
            if existing:
                Submission.objects.filter(conference=existing).delete()
                existing.delete()

        if Conference.objects.filter(code=CODE).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Conference '{CODE}' already exists. Use --force to recreate."
                )
            )
            return

        organizer = self._create_organizer()
        languages = self._create_languages()
        topics = self._create_topics()
        audience_levels = self._create_audience_levels()
        submission_types = self._create_submission_types()
        tags = self._create_tags()
        conference = self._create_conference(
            organizer, languages, topics, audience_levels, submission_types
        )
        durations = self._create_durations(conference, submission_types)
        self._create_deadlines(conference)
        speakers = self._create_speakers()
        self._create_submissions(
            conference,
            speakers,
            languages,
            topics,
            audience_levels,
            submission_types,
            durations,
            tags,
        )
        self._create_sponsors(conference)

        self.stdout.write(self.style.SUCCESS(f"Created conference '{CODE}'."))

    def _create_organizer(self):
        organizer, _ = Organizer.objects.get_or_create(
            slug="python-italia",
            defaults={"name": "Python Italia"},
        )
        return organizer

    def _create_languages(self):
        en, _ = Language.objects.get_or_create(code="en", defaults={"name": "English"})
        it, _ = Language.objects.get_or_create(code="it", defaults={"name": "Italian"})
        return {"en": en, "it": it}

    def _create_topics(self):
        return [Topic.objects.get_or_create(name=name)[0] for name in TOPICS]

    def _create_audience_levels(self):
        return [
            AudienceLevel.objects.get_or_create(name=name)[0]
            for name in AUDIENCE_LEVELS
        ]

    def _create_submission_types(self):
        return {
            name: SubmissionType.objects.get_or_create(name=name)[0]
            for name in SUBMISSION_TYPES
        }

    def _create_tags(self):
        return [SubmissionTag.objects.get_or_create(name=name)[0] for name in TAG_NAMES]

    def _create_conference(
        self, organizer, languages, topics, audience_levels, submission_types
    ):
        now = timezone.now()
        conference = Conference.objects.create(
            organizer=organizer,
            name=LazyI18nString({"en": "PyCon Demo", "it": "PyCon Prova"}),
            code=CODE,
            timezone="Europe/Rome",
            introduction=LazyI18nString(
                {
                    "en": "This is a demo conference seeded for local development.",
                    "it": "Conferenza dimostrativa per sviluppo locale.",
                }
            ),
            location="Florence, Italy",
            start=now + timedelta(days=60),
            end=now + timedelta(days=63),
            latitude=43.766140,
            longitude=11.269985,
            map_link="https://goo.gl/maps/ogYFG5yr7rSHFr586",
        )

        conference.topics.set(topics)
        conference.languages.set(languages.values())
        conference.audience_levels.set(audience_levels)
        conference.submission_types.set(submission_types.values())
        return conference

    def _create_durations(self, conference, submission_types):
        durations = {}
        for mins in (30, 45, 60, 180):
            duration = Duration.objects.create(
                conference=conference,
                name=str(mins),
                duration=mins,
                notes=f"{mins} minutes",
            )
            duration.allowed_submission_types.set(submission_types.values())
            durations[mins] = duration
        return durations

    def _create_deadlines(self, conference):
        now = timezone.now()
        Deadline.objects.create(
            conference=conference,
            type=Deadline.TYPES.cfp,
            name=LazyI18nString(
                {"en": "Call for Proposals", "it": "Call for Proposals"}
            ),
            description=LazyI18nString(
                {"en": "Submit your talks", "it": "Invia le tue proposte"}
            ),
            start=now - timedelta(days=10),
            end=now + timedelta(days=20),
        )
        Deadline.objects.create(
            conference=conference,
            type=Deadline.TYPES.voting,
            name=LazyI18nString({"en": "Community Voting"}),
            start=now + timedelta(days=21),
            end=now + timedelta(days=35),
        )

    def _create_speakers(self):
        speakers = []
        if not User.objects.filter(email="admin@admin.com").exists():
            User.objects.create_superuser("admin@admin.com", "change-on-deploy")

        for email, name in SPEAKERS:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"full_name": name, "name": name.split()[0]},
            )
            if created:
                user.set_password("test")
                user.save()
            speakers.append(user)
        return speakers

    def _create_submissions(
        self,
        conference,
        speakers,
        languages,
        topics,
        audience_levels,
        submission_types,
        durations,
        tags,
    ):
        en = languages["en"]
        for index, (title, type_name, duration_mins) in enumerate(TALKS):
            submission = Submission.objects.create(
                conference=conference,
                speaker=speakers[index % len(speakers)],
                title=LazyI18nString({"en": title}),
                abstract=LazyI18nString({"en": f"Abstract for: {title}"}),
                elevator_pitch=LazyI18nString({"en": f"Elevator pitch for: {title}"}),
                slug=slugify(title),
                speaker_level=Submission.SPEAKER_LEVELS.intermediate,
                topic=topics[index % len(topics)],
                type=submission_types[type_name],
                duration=durations[duration_mins],
                audience_level=audience_levels[index % len(audience_levels)],
                status=Submission.STATUS.proposed,
            )
            submission.languages.add(en)
            submission.tags.add(tags[index % len(tags)])

    def _create_sponsors(self, conference):
        levels = {}
        for name, price, color in SPONSOR_LEVELS:
            level, _ = SponsorLevel.objects.get_or_create(
                conference=conference,
                name=name,
                defaults={"price": price, "highlight_color": color},
            )
            levels[name] = level

        for name, link, level_name in SPONSORS:
            sponsor, _ = Sponsor.objects.get_or_create(
                name=name,
                defaults={"link": link},
            )
            sponsor.levels.add(levels[level_name])
