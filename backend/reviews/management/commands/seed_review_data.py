import random
import uuid

from django.core.management.base import BaseCommand
from django.utils import timezone

from conferences.models import AudienceLevel, Conference, Duration, Topic
from grants.models import Grant
from i18n.strings import LazyI18nString
from languages.models import Language
from organizers.models import Organizer
from reviews.models import AvailableScoreOption, ReviewSession, UserReview
from submissions.models import Submission, SubmissionTag, SubmissionType
from helpers.constants import GENDERS
from users.models import User

GENDER_CHOICES = [g[0] for g in GENDERS]

SCORE_OPTIONS = [
    (-2, "Absolutely not"),
    (-1, "Not convinced"),
    (0, "Maybe"),
    (1, "Good"),
    (2, "Must have"),
]

TALK_TITLES = [
    "Building Scalable APIs with FastAPI",
    "Introduction to Machine Learning with Python",
    "Django Ninja: The New Kid on the Block",
    "Async Python: Beyond the Basics",
    "Type Hints Best Practices",
    "Testing Strategies for Python Projects",
    "Data Pipelines with Apache Airflow",
    "WebAssembly and Python",
    "Deploying ML Models in Production",
    "GraphQL vs REST: A Python Perspective",
    "Python Performance Optimization",
    "Building CLI Tools with Typer",
    "Observability for Python Services",
    "Rust Extensions for Python",
    "Pandas 2.0: What's New",
    "Event-Driven Architecture with Python",
    "Securing Django Applications",
    "Python in the Browser with PyScript",
    "Distributed Systems with Celery",
    "Property-Based Testing with Hypothesis",
]

REVIEWER_NAMES = [
    "Alice Johnson",
    "Bob Smith",
    "Clara Martinez",
    "David Kim",
    "Elena Rossi",
    "Frank Weber",
    "Giulia Bianchi",
    "Hans Mueller",
]


class Command(BaseCommand):
    help = "Seed the database with review session data for local development"

    def add_arguments(self, parser):
        parser.add_argument(
            "--submissions",
            type=int,
            default=20,
            help="Number of submissions to create (default: 20)",
        )
        parser.add_argument(
            "--reviewers",
            type=int,
            default=5,
            help="Number of reviewers to create (default: 5)",
        )
        parser.add_argument(
            "--grants",
            type=int,
            default=15,
            help="Number of grant applications to create (default: 15)",
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all previously seeded review data before creating new data",
        )

    def handle(self, *args, **options):
        num_submissions = options["submissions"]
        num_reviewers = options["reviewers"]
        num_grants = options["grants"]

        if options["flush"]:
            self._flush()

        uid = uuid.uuid4().hex[:6]

        self.stdout.write("Creating conference...")
        conference = self._create_conference(uid)
        self.stdout.write(f"  Conference: {conference.name} ({conference.code})")

        self.stdout.write(f"Creating {num_reviewers} reviewers...")
        reviewers = self._create_reviewers(num_reviewers, uid)
        for r in reviewers:
            self.stdout.write(f"  Reviewer: {r.full_name} ({r.email})")

        self._create_proposals_review(conference, reviewers, num_submissions)
        self._create_grants_review(conference, reviewers, num_grants)

        self.stdout.write(self.style.SUCCESS("\nDone! Review data has been seeded."))

    def _flush(self):
        self.stdout.write("Flushing previous seed data...")
        UserReview.objects.all().delete()
        AvailableScoreOption.objects.all().delete()
        ReviewSession.objects.all().delete()
        Submission.objects.all().delete()
        self.stdout.write("  Flushed.")

    def _create_conference(self, uid):
        organizer, _ = Organizer.objects.get_or_create(
            name=f"PyCon Seed {uid}",
            defaults={"slug": f"pycon-seed-{uid}"},
        )

        conference = Conference.objects.create(
            organizer=organizer,
            name=LazyI18nString({"en": f"PyCon Seed {uid}"}),
            code=f"seed-{uid}",
            introduction=LazyI18nString({"en": "Seeded conference for local dev"}),
            start=timezone.now() - timezone.timedelta(days=30),
            end=timezone.now() + timezone.timedelta(days=30),
            timezone="Europe/Rome",
            pretix_organizer_id=f"seed-org-{uid}",
            pretix_event_id=f"seed-event-{uid}",
        )

        for topic_name in ["Python", "Web", "Data Science", "DevOps"]:
            topic, _ = Topic.objects.get_or_create(name=topic_name)
            conference.topics.add(topic)

        en, _ = Language.objects.get_or_create(
            code="en", defaults={"name": "English"}
        )
        conference.languages.add(en)

        for st_name in ["talk", "tutorial"]:
            st, _ = SubmissionType.objects.get_or_create(name=st_name)
            conference.submission_types.add(st)

        for dur_mins in [30, 45, 60]:
            duration, _ = Duration.objects.get_or_create(
                duration=dur_mins,
                conference=conference,
                defaults={"name": f"{dur_mins}m"},
            )
            duration.allowed_submission_types.set(SubmissionType.objects.all())
            conference.durations.add(duration)

        for al_name in ["Beginner", "Intermediate", "Advanced"]:
            al, _ = AudienceLevel.objects.get_or_create(name=al_name)
            conference.audience_levels.add(al)

        return conference

    def _create_reviewers(self, count, uid):
        reviewers = []
        for i in range(count):
            name = REVIEWER_NAMES[i % len(REVIEWER_NAMES)]
            email = f"reviewer-{uid}-{i}@example.org"
            user = User.objects.create_user(
                email=email,
                password="test",
                full_name=name,
                username=f"reviewer-{uid}-{i}",
                is_staff=True,
                is_superuser=True,
            )
            reviewers.append(user)
        return reviewers

    def _create_submissions(self, conference, count):
        en = Language.objects.get(code="en")
        submission_type = conference.submission_types.first()
        duration = conference.durations.first()
        audience_level = conference.audience_levels.first()
        topic = conference.topics.first()
        tag_names = ["python", "web", "data", "testing", "devops", "ml", "api"]

        # Create some speakers with multiple submissions to test the
        # "speaker has multiple talks" feature
        multi_submission_speakers = []
        num_multi_speakers = min(3, count // 4)  # ~25% of submissions from repeat speakers
        for i in range(num_multi_speakers):
            speaker = User.objects.create_user(
                email=f"multi-speaker-{uuid.uuid4().hex[:8]}@example.org",
                password="test",
                full_name=f"Multi-Talk Speaker {i}",
                username=f"multi-speaker-{uuid.uuid4().hex[:8]}",
                gender=random.choice(GENDER_CHOICES),
            )
            # Each multi-speaker will have 2-3 submissions
            num_talks = random.randint(2, 3)
            multi_submission_speakers.append((speaker, num_talks))

        # Calculate how many single-speaker submissions we need
        multi_speaker_submissions = sum(n for _, n in multi_submission_speakers)
        single_speaker_count = count - multi_speaker_submissions

        submissions = []
        title_index = 0

        # Create submissions for multi-talk speakers
        for speaker, num_talks in multi_submission_speakers:
            for _ in range(num_talks):
                title = TALK_TITLES[title_index % len(TALK_TITLES)]
                title_index += 1
                submission = Submission.objects.create(
                    conference=conference,
                    speaker=speaker,
                    title=LazyI18nString({"en": title}),
                    abstract=LazyI18nString({"en": f"Abstract for {title}"}),
                    elevator_pitch=LazyI18nString(
                        {"en": f"A talk about {title.lower()}"}
                    ),
                    notes=f"Speaker notes for {title}",
                    type=submission_type,
                    duration=duration,
                    topic=topic,
                    audience_level=audience_level,
                    speaker_level=random.choice(
                        [c[0] for c in Submission.SPEAKER_LEVELS]
                    ),
                    status="proposed",
                )
                submission.languages.add(en)
                selected_tags = random.sample(tag_names, k=random.randint(1, 3))
                for tag_name in selected_tags:
                    tag, _ = SubmissionTag.objects.get_or_create(name=tag_name)
                    submission.tags.add(tag)
                submissions.append(submission)

        # Create single-speaker submissions
        for i in range(single_speaker_count):
            title = TALK_TITLES[title_index % len(TALK_TITLES)]
            title_index += 1
            speaker = User.objects.create_user(
                email=f"speaker-{uuid.uuid4().hex[:8]}@example.org",
                password="test",
                full_name=f"Speaker {i}",
                username=f"speaker-{uuid.uuid4().hex[:8]}",
                gender=random.choice(GENDER_CHOICES),
            )
            submission = Submission.objects.create(
                conference=conference,
                speaker=speaker,
                title=LazyI18nString({"en": title}),
                abstract=LazyI18nString({"en": f"Abstract for {title}"}),
                elevator_pitch=LazyI18nString(
                    {"en": f"A talk about {title.lower()}"}
                ),
                notes=f"Speaker notes for {title}",
                type=submission_type,
                duration=duration,
                topic=topic,
                audience_level=audience_level,
                speaker_level=random.choice(
                    [c[0] for c in Submission.SPEAKER_LEVELS]
                ),
                status="proposed",
            )
            submission.languages.add(en)
            selected_tags = random.sample(tag_names, k=random.randint(1, 3))
            for tag_name in selected_tags:
                tag, _ = SubmissionTag.objects.get_or_create(name=tag_name)
                submission.tags.add(tag)
            submissions.append(submission)

        return submissions

    def _create_score_options(self, review_session):
        score_options = {}
        for i, (value, label) in enumerate(SCORE_OPTIONS):
            score_options[value] = AvailableScoreOption.objects.create(
                review_session=review_session,
                numeric_value=value,
                label=label,
                order=i,
            )
        return score_options

    def _create_grants(self, conference, count):
        occupations = [c[0] for c in Grant.Occupation.choices]
        age_groups = [c[0] for c in Grant.AgeGroup.choices]
        grant_types = [c[0] for c in Grant.GrantType.choices]

        grants = []
        for i in range(count):
            user = User.objects.create_user(
                email=f"grantee-{uuid.uuid4().hex[:8]}@example.org",
                password="test",
                full_name=f"Grant Applicant {i}",
                username=f"grantee-{uuid.uuid4().hex[:8]}",
                gender=random.choice(GENDER_CHOICES),
            )
            grant = Grant.objects.create(
                conference=conference,
                user=user,
                email=user.email,
                full_name=user.full_name,
                name=f"Applicant {i}",
                age_group=random.choice(age_groups),
                occupation=random.choice(occupations),
                grant_type=random.sample(grant_types, k=random.randint(1, 2)),
                python_usage=f"I use Python for {random.choice(['web dev', 'data science', 'automation', 'ML', 'teaching'])}.",
                been_to_other_events=random.choice(["Yes, PyCon US", "No", "EuroPython 2023"]),
                needs_funds_for_travel=random.choice([True, False]),
                why=f"I want to attend because {random.choice(['I want to learn', 'I want to network', 'I want to speak', 'I love Python'])}.",
                departure_country=random.choice(["IT", "DE", "FR", "US", "GB", "ES"]),
                departure_city=random.choice(["Rome", "Berlin", "Paris", "New York", "London", "Madrid"]),
                nationality=random.choice(["Italian", "German", "French", "American", "British", "Spanish"]),
            )
            grants.append(grant)

        return grants

    def _create_proposals_review(self, conference, reviewers, num_submissions):
        self.stdout.write("\n--- Proposals Review Session ---")

        review_session = ReviewSession.objects.create(
            conference=conference,
            session_type="proposals",
            status="draft",
        )
        self.stdout.write(f"  Review session ID: {review_session.id}")

        score_options = self._create_score_options(review_session)

        self.stdout.write(f"Creating {num_submissions} submissions (some speakers will have multiple talks)...")
        submissions = self._create_submissions(conference, num_submissions)

        self.stdout.write(f"Creating reviews for {len(submissions)} submissions...")
        for submission in submissions:
            num_reviews = random.randint(2, len(reviewers))
            selected_reviewers = random.sample(reviewers, num_reviews)
            for reviewer in selected_reviewers:
                score_value = random.choices(
                    list(score_options.keys()),
                    weights=[5, 15, 30, 35, 15],
                )[0]
                UserReview.objects.create(
                    review_session=review_session,
                    user=reviewer,
                    proposal=submission,
                    score=score_options[score_value],
                )

        review_session.status = "reviewing"
        review_session.save()
        self.stdout.write(
            f"  Proposals review session ready (ID: {review_session.id})"
        )

    def _create_grants_review(self, conference, reviewers, num_grants):
        self.stdout.write("\n--- Grants Review Session ---")

        review_session = ReviewSession.objects.create(
            conference=conference,
            session_type="grants",
            status="draft",
        )

        score_options = self._create_score_options(review_session)

        self.stdout.write(f"Creating {num_grants} grant applications...")
        grants = self._create_grants(conference, num_grants)

        self.stdout.write(f"Creating reviews for {len(grants)} grants...")
        for grant in grants:
            num_reviews = random.randint(2, len(reviewers))
            selected_reviewers = random.sample(reviewers, num_reviews)
            for reviewer in selected_reviewers:
                score_value = random.choices(
                    list(score_options.keys()),
                    weights=[10, 20, 30, 25, 15],
                )[0]
                UserReview.objects.create(
                    review_session=review_session,
                    user=reviewer,
                    grant=grant,
                    score=score_options[score_value],
                )

        review_session.status = "reviewing"
        review_session.save()
        self.stdout.write(f"  Grants review session ready (ID: {review_session.id})")
