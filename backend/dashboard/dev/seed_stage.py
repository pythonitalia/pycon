"""Seed the local dashboard and Pretix with deterministic stage data.

This file is executed through ``manage.py shell`` by scripts/seed-dashboard-stage.
It is deliberately guarded so it cannot target a hosted Pretix instance.
"""

import math
import os
from datetime import UTC, datetime, time, timedelta
from decimal import Decimal
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from conferences.models import AudienceLevel, Conference, Deadline, Duration, Topic
from grants.models import Grant, GrantReimbursement, GrantReimbursementCategory
from i18n.strings import LazyI18nString
from languages.models import Language
from organizers.models import Organizer
from reviews.models import UserReview
from submissions.models import Submission, SubmissionType
from users.models import User
from voting.models import Vote

CONFERENCE_CODE = "dashboard-local"
ORGANIZER_SLUG = "python-italia-local"

STAGES = {
    "cfp-open": {
        "conference_offset": 180,
        "deadlines": {
            "cfp": (-14, 28),
            "voting": (35, 49),
            "grants": (-7, 42),
            "custom": (84, 90),
        },
        "proposals": {"proposed": 54},
        "grants": {"pending": 12},
        "votes": 0,
        "tickets": 0,
        "active_weeks": 3,
    },
    "review": {
        "conference_offset": 120,
        "deadlines": {
            "cfp": (-70, -28),
            "voting": (-7, 14),
            "grants": (-35, 14),
            "custom": (28, 35),
        },
        "proposals": {"proposed": 186},
        "grants": {"pending": 48},
        "votes": 1260,
        "tickets": 80,
        "active_weeks": 8,
    },
    "ticket-sales": {
        "conference_offset": 60,
        "deadlines": {
            "cfp": (-120, -80),
            "voting": (-70, -50),
            "grants": (-95, -45),
            "custom": (-35, -28),
        },
        "proposals": {
            "accepted": 42,
            "waiting_list": 12,
            "rejected": 151,
            "cancelled": 9,
        },
        "grants": {
            "approved": 10,
            "waiting_for_confirmation": 8,
            "confirmed": 20,
            "waiting_list": 12,
            "rejected": 26,
        },
        "votes": 1700,
        "tickets": 480,
        "active_weeks": 8,
    },
    "conference-week": {
        "conference_offset": -1,
        "deadlines": {
            "cfp": (-230, -190),
            "voting": (-170, -150),
            "grants": (-205, -145),
            "custom": (-105, -98),
        },
        "proposals": {
            "accepted": 45,
            "waiting_list": 8,
            "rejected": 160,
            "cancelled": 9,
        },
        "grants": {
            "approved": 4,
            "waiting_for_confirmation": 3,
            "confirmed": 45,
            "waiting_list": 8,
            "refused": 4,
            "rejected": 20,
        },
        "votes": 1850,
        "tickets": 960,
        "active_weeks": 8,
    },
    "post-event": {
        "conference_offset": -35,
        "deadlines": {
            "cfp": (-265, -225),
            "voting": (-205, -185),
            "grants": (-240, -180),
            "custom": (-140, -133),
        },
        "proposals": {
            "accepted": 46,
            "waiting_list": 7,
            "rejected": 163,
            "cancelled": 10,
        },
        "grants": {
            "confirmed": 47,
            "waiting_list": 6,
            "refused": 6,
            "rejected": 22,
            "did_not_attend": 5,
        },
        "votes": 1900,
        "tickets": 1040,
        "active_weeks": 8,
    },
}

PRODUCTS = (
    {
        "name": "Community ticket",
        "internal_name": "community",
        "price": "199.00",
    },
    {
        "name": "Student ticket",
        "internal_name": "student",
        "price": "99.00",
    },
    {
        "name": "Business ticket",
        "internal_name": "business",
        "price": "399.00",
    },
)


def i18n(value: str) -> LazyI18nString:
    return LazyI18nString({"en": value, "it": value})


def expand_counts(counts: dict[str, int]) -> list[str]:
    return [status for status, count in counts.items() for _ in range(count)]


def spread_timestamps(objects: list, active_weeks: int) -> None:
    if not objects:
        return

    current = timezone.now()
    for index, item in enumerate(objects):
        week = min(active_weeks - 1, index * active_weeks // len(objects))
        weeks_ago = active_weeks - week - 1
        item.created = current - timedelta(
            weeks=weeks_ago,
            days=(index * 3) % 6,
            hours=index % 12,
        )
        item.modified = item.created
    objects[0].__class__.objects.bulk_update(objects, ["created", "modified"])


def create_users(prefix: str, count: int) -> list[User]:
    users = [
        User(
            email=f"dashboard-{prefix}-{index + 1}@dashboard.local",
            username=f"dashboard-{prefix}-{index + 1}",
            full_name=f"Dashboard {prefix.title()} {index + 1}",
            name=f"{prefix.title()} {index + 1}",
            password="!",
        )
        for index in range(count)
    ]
    return User.objects.bulk_create(users)


def seed_django(stage: dict) -> Conference:
    today = timezone.localdate()
    conference_start = timezone.make_aware(
        datetime.combine(
            today + timedelta(days=stage["conference_offset"]),
            time(hour=9),
        ),
        timezone=timezone.get_current_timezone(),
    )
    conference_end = conference_start + timedelta(days=3, hours=9)

    with transaction.atomic():
        existing_conference = Conference.objects.filter(code=CONFERENCE_CODE).first()
        if existing_conference is not None:
            Submission.objects.filter(conference=existing_conference).delete()
            UserReview.objects.filter(grant__conference=existing_conference).delete()
            GrantReimbursement.objects.filter(
                grant__conference=existing_conference
            ).delete()
            Grant.objects.filter(conference=existing_conference)._raw_delete(
                using=Grant.objects.db
            )
            existing_conference.delete()
        User.objects.filter(
            email__startswith="dashboard-",
            email__endswith="@dashboard.local",
        ).delete()

        organizer, _ = Organizer.objects.get_or_create(
            slug=ORGANIZER_SLUG,
            defaults={"name": "Python Italia local"},
        )
        conference = Conference.objects.create(
            organizer=organizer,
            name=i18n("PyCon Italia dashboard playground"),
            introduction=i18n("Local-only data for dashboard development."),
            code=CONFERENCE_CODE,
            hostname="dashboard.localhost",
            location="Bologna, Italy",
            timezone="Europe/Rome",
            start=conference_start,
            end=conference_end,
            pretix_organizer_id=ORGANIZER_SLUG,
            pretix_event_id=CONFERENCE_CODE,
            pretix_event_url=(
                f"http://localhost:8345/{ORGANIZER_SLUG}/{CONFERENCE_CODE}/"
            ),
        )

        deadline_names = {
            "cfp": "Call for proposals",
            "voting": "Community voting",
            "grants": "Financial aid",
            "custom": "Schedule announced",
        }
        for deadline_type, offsets in stage["deadlines"].items():
            Deadline.objects.create(
                conference=conference,
                type=deadline_type,
                name=i18n(deadline_names[deadline_type]),
                description=i18n(f"Local {deadline_names[deadline_type]} stage."),
                start=timezone.now() + timedelta(days=offsets[0]),
                end=timezone.now() + timedelta(days=offsets[1]),
            )

        submission_type, _ = SubmissionType.objects.get_or_create(name="Dashboard talk")
        audience_level, _ = AudienceLevel.objects.get_or_create(
            name="Dashboard intermediate"
        )
        topic, _ = Topic.objects.get_or_create(name="Dashboard Python")
        duration = Duration.objects.create(
            conference=conference,
            name="30 minutes",
            duration=30,
            notes="Local dashboard seed",
        )
        duration.allowed_submission_types.add(submission_type)
        conference.submission_types.add(submission_type)
        conference.audience_levels.add(audience_level)
        conference.topics.add(topic)
        languages = Language.objects.filter(code__in=("en", "it"))
        conference.languages.add(*languages)

        proposal_statuses = expand_counts(stage["proposals"])
        speakers = create_users("speaker", len(proposal_statuses))
        submissions = Submission.objects.bulk_create(
            [
                Submission(
                    conference=conference,
                    title=i18n(f"Practical Python story {index + 1}"),
                    abstract=i18n(
                        "A realistic local proposal used to exercise dashboard trends."
                    ),
                    elevator_pitch=i18n("Useful Python lessons from production."),
                    slug=f"dashboard-proposal-{index + 1}",
                    speaker_level=("new", "intermediate", "experienced")[index % 3],
                    previous_talk_video="",
                    speaker=speakers[index],
                    topic=topic,
                    type=submission_type,
                    duration=duration,
                    audience_level=audience_level,
                    status=status,
                )
                for index, status in enumerate(proposal_statuses)
            ]
        )
        spread_timestamps(submissions, stage["active_weeks"])

        grant_statuses = expand_counts(stage["grants"])
        applicants = create_users("applicant", len(grant_statuses))
        grants = Grant.objects.bulk_create(
            [
                Grant(
                    conference=conference,
                    user=applicants[index],
                    email=applicants[index].email,
                    full_name=f"Dashboard Applicant {index + 1}",
                    name=f"Applicant {index + 1}",
                    age_group=Grant.AgeGroup.range_25_34,
                    occupation=Grant.Occupation.developer,
                    grant_type=[Grant.GrantType.diversity],
                    departure_country="IT",
                    nationality="Italian",
                    departure_city="Bologna",
                    needs_funds_for_travel=index % 3 != 0,
                    need_accommodation=index % 2 == 0,
                    why="Attending would support my local Python community work.",
                    python_usage="I use Python for web and data projects.",
                    been_to_other_events="A mix of local meetups and conferences.",
                    status=status,
                )
                for index, status in enumerate(grant_statuses)
            ]
        )
        spread_timestamps(grants, stage["active_weeks"])

        ticket_category = GrantReimbursementCategory.objects.create(
            conference=conference,
            name="Ticket",
            category=GrantReimbursementCategory.Category.TICKET,
            max_amount=Decimal(199),
            included_by_default=True,
        )
        travel_category = GrantReimbursementCategory.objects.create(
            conference=conference,
            name="Travel",
            category=GrantReimbursementCategory.Category.TRAVEL,
            max_amount=Decimal(700),
        )
        allocated_statuses = {
            Grant.Status.approved,
            Grant.Status.waiting_for_confirmation,
            Grant.Status.confirmed,
        }
        reimbursements = []
        for index, grant in enumerate(grants):
            if grant.status not in allocated_statuses:
                continue
            reimbursements.append(
                GrantReimbursement(
                    grant=grant,
                    category=ticket_category,
                    granted_amount=Decimal(199),
                )
            )
            if index % 3 != 0:
                reimbursements.append(
                    GrantReimbursement(
                        grant=grant,
                        category=travel_category,
                        granted_amount=Decimal(str(250 + (index % 5) * 75)),
                    )
                )
        GrantReimbursement.objects.bulk_create(reimbursements)

        if stage["votes"]:
            voter_count = math.ceil(stage["votes"] / len(submissions))
            voters = create_users("voter", voter_count)
            votes = [
                Vote(
                    user=voters[index // len(submissions)],
                    submission=submissions[index % len(submissions)],
                    value=(index % 4) + 1,
                )
                for index in range(stage["votes"])
            ]
            Vote.objects.bulk_create(votes)

    return conference


class PretixAPI:
    def __init__(self) -> None:
        parsed = urlparse(settings.PRETIX_API)
        if parsed.hostname not in {"pretix", "localhost", "127.0.0.1"}:
            raise RuntimeError(
                "The dashboard stage seeder refuses to target a non-local Pretix API."
            )

        self.base_url = settings.PRETIX_API.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Token {settings.PRETIX_API_TOKEN}",
                "Host": settings.PRETIX_API_HOST or "localhost:8345",
            }
        )

    def request(self, method: str, path: str, **kwargs) -> dict:
        response = self.session.request(
            method,
            f"{self.base_url}/{path.lstrip('/')}",
            timeout=settings.PRETIX_API_TIMEOUT,
            **kwargs,
        )
        if not response.ok:
            raise RuntimeError(
                f"Pretix {method} {path} returned {response.status_code}: "
                f"{response.text[:1000]}"
            )
        return response.json() if response.content else {}


def order_week(index: int, total: int) -> int:
    weights = (2, 4, 6, 9, 12, 16, 21, 30)
    target = index * sum(weights) / max(total, 1)
    cumulative = 0
    for week, weight in enumerate(weights):
        cumulative += weight
        if target < cumulative:
            return week
    return len(weights) - 1


def seed_pretix(stage: dict, conference: Conference) -> None:
    api = PretixAPI()
    organizer_path = f"organizers/{ORGANIZER_SLUG}"
    event_path = f"{organizer_path}/events/{CONFERENCE_CODE}"
    event = api.request(
        "POST",
        f"{organizer_path}/events/",
        json={
            "name": {"en": "PyCon Italia dashboard playground"},
            "slug": CONFERENCE_CODE,
            "live": False,
            "testmode": False,
            "currency": "EUR",
            "date_from": conference.start.isoformat(),
            "date_to": conference.end.isoformat(),
            "is_public": False,
            "location": {"en": "Bologna, Italy"},
            "timezone": "Europe/Rome",
            "plugins": [
                "pretix.plugins.sendmail",
                "pretix.plugins.statistics",
                "pretix.plugins.banktransfer",
            ],
        },
    )

    items = []
    for position, product in enumerate(PRODUCTS):
        items.append(
            api.request(
                "POST",
                f"{event_path}/items/",
                json={
                    "name": {"en": product["name"]},
                    "internal_name": product["internal_name"],
                    "active": True,
                    "default_price": product["price"],
                    "admission": True,
                    "personalized": True,
                    "position": position,
                },
            )
        )

    api.request(
        "POST",
        f"{event_path}/quotas/",
        json={
            "name": "Conference capacity",
            "size": max(250, stage["tickets"] + 250),
            "items": [item["id"] for item in items],
            "variations": [],
            "closed": False,
            "close_when_sold_out": False,
        },
    )
    position_pattern = (2, 4, 3, 4)
    remaining = stage["tickets"]
    order_sizes = []
    order_index = 0
    while remaining:
        size = min(position_pattern[order_index % len(position_pattern)], remaining)
        order_sizes.append(size)
        remaining -= size
        order_index += 1

    current_monday = timezone.localdate() - timedelta(
        days=timezone.localdate().weekday()
    )
    ticket_index = 0
    for index, size in enumerate(order_sizes):
        week = order_week(index, len(order_sizes))
        week_start = current_monday - timedelta(weeks=7 - week)
        ordered_at = datetime.combine(
            week_start + timedelta(days=(index * 3) % 7),
            time(hour=10 + index % 8),
            tzinfo=UTC,
        )
        positions = []
        for _ in range(size):
            roll = (ticket_index * 37) % 100
            item_index = 0 if roll < 65 else 1 if roll < 85 else 2
            positions.append(
                {
                    "item": items[item_index]["id"],
                    "attendee_name": f"Local Attendee {ticket_index + 1}",
                }
            )
            ticket_index += 1

        api.request(
            "POST",
            f"{event_path}/orders/",
            json={
                "status": "p",
                "testmode": False,
                "locale": "en",
                "payment_provider": "banktransfer",
                "positions": positions,
                "force": True,
                "send_email": False,
                "api_meta": {
                    "dashboard_seed_ordered_at": ordered_at.isoformat(),
                },
            },
        )
        if (index + 1) % 50 == 0:
            print(f"Created {index + 1}/{len(order_sizes)} local Pretix orders...")

    print(
        f"Created Pretix event {event['slug']} with {stage['tickets']} paid tickets "
        f"across {len(order_sizes)} orders."
    )


if not settings.DEBUG:
    raise RuntimeError("Dashboard stage data can only be seeded with DEBUG enabled.")

stage_name = os.environ.get("DASHBOARD_STAGE", "")
if stage_name not in STAGES:
    raise ValueError(
        f"Unknown DASHBOARD_STAGE {stage_name!r}. Choose from: {', '.join(STAGES)}"
    )

selected_stage = STAGES[stage_name]
seeded_conference = seed_django(selected_stage)
seed_pretix(selected_stage, seeded_conference)
cache.clear()
print(
    f"Seeded {stage_name}: {sum(selected_stage['proposals'].values())} proposals, "
    f"{sum(selected_stage['grants'].values())} grants, "
    f"{selected_stage['votes']} votes, and {selected_stage['tickets']} tickets."
)
