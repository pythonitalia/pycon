"""Durable workflow that creates a new conference from an existing one.

Setting up the next edition means re-creating, by hand, everything that is
configuration rather than content: deadlines, durations, the schedule days
with their rooms and slots, sponsor levels and their benefits, email templates,
menus, copy, forms. The workflow does that in one durable run: every step is a
Resonate durable child, so a crash (or a database hiccup, which Resonate
retries) resumes from the step that failed instead of leaving a half-built
conference behind.

Content produced *during* an edition is never copied: proposals, the talks
scheduled into those slots, keynotes, sponsors, grants, vouchers, answers.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from typing import Any, Callable

from django.db import transaction
from resonate.context import Context

from cms.models import FAQ, GenericCopy, Menu, MenuLink
from conferences.models import Conference, Deadline, Duration
from generic_forms.models import Form, FormQuestion
from notifications.models import EmailTemplate, EmailTemplateIdentifier
from pycon.resonate_app import database_step, get_resonate
from schedule.models import Day, DayRoomThroughModel, Slot
from sponsors.models import (
    SponsorBenefit,
    SponsorLevel,
    SponsorLevelBenefit,
    SponsorSpecialOption,
)
from voting.models import IncludedEvent

resonate = get_resonate()

CLONE_CONFERENCE = "clone_conference"

# Copied verbatim onto the new conference: settings that describe how the
# organizers work, not what happened at a given edition. Anything tied to one
# edition (pretix ids, logo, dates, code, hostname) is deliberately absent.
CONFERENCE_FIELDS_TO_COPY = (
    "organizer_id",
    "timezone",
    "location",
    "introduction",
    "latitude",
    "longitude",
    "map_link",
    "slack_new_proposal_channel_id",
    "slack_new_grant_reply_channel_id",
    "slack_speaker_invitation_answer_channel_id",
    "slack_new_sponsor_lead_channel_id",
    "slack_new_invitation_letter_request_channel_id",
    "video_title_template",
    "video_description_template",
    "youtube_video_bottom_text",
    "frontend_revalidate_url",
    "frontend_revalidate_secret",
    "max_proposals_per_user",
)

CONFERENCE_TAXONOMIES_TO_COPY = (
    "topics",
    "languages",
    "audience_levels",
    "submission_types",
    "proposal_tags",
)


def i18n_key(value: Any) -> str:
    """A comparable key for an i18n field value.

    i18n fields cannot be used in ORM lookups (they raise), so models keyed on
    one are de-duplicated in Python instead.
    """
    data = getattr(value, "data", value)

    if isinstance(data, dict):
        return json.dumps(data, sort_keys=True)

    return str(data)


def conference_dates(conference: Conference) -> list[date]:
    """Every day the conference runs on, in its own timezone."""
    if not conference.start or not conference.end:
        return []

    start = conference.start.astimezone(conference.timezone).date()
    end = conference.end.astimezone(conference.timezone).date()

    return [start + timedelta(days=offset) for offset in range((end - start).days + 1)]


def copy_step(fn: Callable[[Conference, Conference], int]):
    """Make a durable step out of a function copying one conference's config.

    Every step needs the same two conferences, one transaction around its
    writes, and returns how many objects it created, so that lives here rather
    than in each of them. The step keeps the ``(ctx, source_code,
    conference_id)`` signature the SDK inspects -- which is why it cannot use
    ``functools.wraps``, as that would point the signature back at ``fn``.
    """

    def step(ctx: Context, source_code: str, conference_id: int) -> int:
        with transaction.atomic():
            source = Conference.objects.get(code=source_code)
            conference = Conference.objects.get(id=conference_id)

            return fn(source, conference)

    step.__name__ = fn.__name__
    step.__qualname__ = fn.__qualname__
    step.__doc__ = fn.__doc__

    return database_step(step)


@database_step
def create_conference(
    ctx: Context,
    source_code: str,
    new_code: str,
    new_name: str,
    new_start: datetime,
    new_end: datetime,
    new_hostname: str,
) -> int:
    """Create the new conference (or return the existing one) and its taxonomies."""
    with transaction.atomic():
        source = Conference.objects.get(code=source_code)

        conference, _ = Conference.objects.get_or_create(
            code=new_code,
            defaults={
                "name": new_name,
                "hostname": new_hostname,
                "start": new_start,
                "end": new_end,
                **{
                    field: getattr(source, field) for field in CONFERENCE_FIELDS_TO_COPY
                },
            },
        )

        for taxonomy in CONFERENCE_TAXONOMIES_TO_COPY:
            getattr(conference, taxonomy).set(getattr(source, taxonomy).all())

        return conference.id


@copy_step
def copy_deadlines(source: Conference, conference: Conference) -> int:
    """Copy deadlines, shifted by the gap between the two editions' start dates."""
    if source.start and conference.start:
        shift = conference.start - source.start
    else:
        shift = timedelta()

    copied = 0

    for deadline in source.deadlines.all():
        _, created = Deadline.objects.get_or_create(
            conference=conference,
            type=deadline.type,
            defaults={
                "name": deadline.name,
                "description": deadline.description,
                "start": deadline.start + shift,
                "end": deadline.end + shift,
            },
        )
        copied += int(created)

    return copied


@copy_step
def copy_durations(source: Conference, conference: Conference) -> int:
    copied = 0

    for duration in source.durations.all():
        new_duration, created = Duration.objects.get_or_create(
            conference=conference,
            name=duration.name,
            defaults={
                "duration": duration.duration,
                "notes": duration.notes,
            },
        )
        new_duration.allowed_submission_types.set(
            duration.allowed_submission_types.all()
        )
        copied += int(created)

    return copied


@copy_step
def copy_days(source: Conference, conference: Conference) -> int:
    """Lay the schedule out again over the new conference's own dates.

    The new conference gets one day per date it runs on, and each takes the
    rooms and slots of the source day in the same position, so a conference
    that opens with a workshop day keeps that shape. Days the source edition
    did not have are left empty. Streaming and Sli.do links stay with the
    edition that used them.
    """
    source_days = list(source.days.order_by("day"))
    copied = 0

    for position, day_date in enumerate(conference_dates(conference)):
        day, created = Day.objects.get_or_create(conference=conference, day=day_date)
        copied += int(created)

        if position >= len(source_days):
            continue

        source_day = source_days[position]

        for added_room in source_day.added_rooms.order_by("order"):
            DayRoomThroughModel.objects.get_or_create(day=day, room=added_room.room)

        for slot in source_day.slots.order_by("hour"):
            Slot.objects.get_or_create(
                day=day,
                hour=slot.hour,
                duration=slot.duration,
                type=slot.type,
            )

    return copied


@copy_step
def copy_sponsor_benefits(source: Conference, conference: Conference) -> int:
    existing = {
        i18n_key(benefit.name)
        for benefit in SponsorBenefit.objects.filter(conference=conference)
    }
    copied = 0

    for benefit in source.sponsor_benefits.order_by("order"):
        if i18n_key(benefit.name) in existing:
            continue

        SponsorBenefit.objects.create(
            conference=conference,
            name=benefit.name,
            category=benefit.category,
            description=benefit.description,
        )
        copied += 1

    return copied


@copy_step
def copy_sponsor_levels(source: Conference, conference: Conference) -> int:
    """Copy sponsor levels and which benefits they include (never the sponsors)."""
    benefits_by_name = {
        i18n_key(benefit.name): benefit
        for benefit in SponsorBenefit.objects.filter(conference=conference)
    }
    copied = 0

    for level in source.sponsor_levels.order_by("order"):
        new_level, created = SponsorLevel.objects.get_or_create(
            conference=conference,
            name=level.name,
            defaults={
                "highlight_color": level.highlight_color,
                "price": level.price,
                "slots": level.slots,
            },
        )
        copied += int(created)

        for level_benefit in SponsorLevelBenefit.objects.filter(sponsor_level=level):
            benefit = benefits_by_name.get(i18n_key(level_benefit.benefit.name))

            if benefit is None:
                continue

            SponsorLevelBenefit.objects.get_or_create(
                sponsor_level=new_level,
                benefit=benefit,
                defaults={"value": level_benefit.value},
            )

    return copied


@copy_step
def copy_sponsor_special_options(source: Conference, conference: Conference) -> int:
    copied = 0

    for option in source.sponsor_special_options.order_by("order"):
        _, created = SponsorSpecialOption.objects.get_or_create(
            conference=conference,
            name=option.name,
            defaults={
                "description": option.description,
                "price": option.price,
            },
        )
        copied += int(created)

    return copied


@copy_step
def copy_email_templates(source: Conference, conference: Conference) -> int:
    copied = 0

    for template in source.email_templates.all():
        lookup = {"conference": conference, "identifier": template.identifier}

        # Only custom templates can repeat an identifier, so they are told
        # apart by name.
        if template.identifier == EmailTemplateIdentifier.custom:
            lookup["name"] = template.name

        _, created = EmailTemplate.objects.get_or_create(
            **lookup,
            defaults={
                "name": template.name,
                "reply_to": template.reply_to,
                "subject": template.subject,
                "preview_text": template.preview_text,
                "body": template.body,
                "cc_addresses": template.cc_addresses,
                "bcc_addresses": template.bcc_addresses,
            },
        )
        copied += int(created)

    return copied


@copy_step
def copy_cms_content(source: Conference, conference: Conference) -> int:
    """Copy generic copy, FAQs and menus (with their links)."""
    return (
        copy_generic_copy(source, conference)
        + copy_faqs(source, conference)
        + copy_menus(source, conference)
    )


def copy_generic_copy(source: Conference, conference: Conference) -> int:
    copied = 0

    for copy in source.copy.all():
        _, created = GenericCopy.objects.get_or_create(
            conference=conference,
            key=copy.key,
            defaults={"content": copy.content},
        )
        copied += int(created)

    return copied


def copy_faqs(source: Conference, conference: Conference) -> int:
    existing = {
        i18n_key(faq.question) for faq in FAQ.objects.filter(conference=conference)
    }
    copied = 0

    for faq in source.faqs.all():
        if i18n_key(faq.question) in existing:
            continue

        FAQ.objects.create(
            conference=conference, question=faq.question, answer=faq.answer
        )
        copied += 1

    return copied


def copy_menus(source: Conference, conference: Conference) -> int:
    copied = 0

    for menu in source.menus.all():
        new_menu, created = Menu.objects.get_or_create(
            conference=conference,
            identifier=menu.identifier,
            defaults={"title": menu.title},
        )
        copied += int(created)

        existing_links = {i18n_key(link.title) for link in new_menu.links.all()}

        for link in menu.links.order_by("order"):
            if i18n_key(link.title) in existing_links:
                continue

            MenuLink.objects.create(
                menu=new_menu,
                title=link.title,
                href=link.href,
                is_primary=link.is_primary,
            )
            copied += 1

    return copied


@copy_step
def copy_forms(source: Conference, conference: Conference) -> int:
    """Copy forms and their questions; answers belong to the old edition."""
    copied = 0

    for form in source.forms.all():
        new_form, created = Form.objects.get_or_create(
            conference=conference,
            purpose=form.purpose,
            name=form.name,
        )
        copied += int(created)

        for question in form.questions.all():
            _, question_created = FormQuestion.objects.get_or_create(
                form=new_form,
                label=question.label,
                defaults={
                    "description": question.description,
                    "question_type": question.question_type,
                    "options": question.options,
                    "required": question.required,
                    "max_length": question.max_length,
                    "order": question.order,
                    "active": question.active,
                },
            )
            copied += int(question_created)

    return copied


@copy_step
def copy_voting_included_events(source: Conference, conference: Conference) -> int:
    copied = 0

    for included_event in source.included_voting_events.all():
        _, created = IncludedEvent.objects.get_or_create(
            conference=conference,
            pretix_organizer_id=included_event.pretix_organizer_id,
            pretix_event_id=included_event.pretix_event_id,
        )
        copied += int(created)

    return copied


# Everything that only needs the source and the freshly created conference,
# in the order it is copied. Sponsor levels read the benefits copied just
# before them, so the order matters. The names are what the workflow reports
# back as its `copied` counts, so they are spelled out rather than derived from
# the functions: renaming one should not change what callers read.
COPY_STEPS = (
    ("deadlines", copy_deadlines),
    ("durations", copy_durations),
    ("days", copy_days),
    ("sponsor_benefits", copy_sponsor_benefits),
    ("sponsor_levels", copy_sponsor_levels),
    ("sponsor_special_options", copy_sponsor_special_options),
    ("email_templates", copy_email_templates),
    ("cms_content", copy_cms_content),
    ("forms", copy_forms),
    ("voting_included_events", copy_voting_included_events),
)


@resonate.register(name=CLONE_CONFERENCE)
async def clone_conference(
    ctx: Context,
    source_code: str,
    new_code: str,
    new_name: str,
    new_start: datetime,
    new_end: datetime,
    new_hostname: str,
) -> dict[str, Any]:
    """Create ``new_code`` using ``source_code`` as its base.

    Re-running with the same workflow id joins the original run; re-running
    with a new id against a conference that already exists tops up whatever is
    missing, since every step only creates what is not there yet.
    """
    conference_id: int = await ctx.run(
        create_conference,
        source_code,
        new_code,
        new_name,
        new_start,
        new_end,
        new_hostname,
    )

    copied: dict[str, int] = {}

    for name, step in COPY_STEPS:
        copied[name] = await ctx.run(step, source_code, conference_id)

    return {
        "conference_id": conference_id,
        "code": new_code,
        "copied": copied,
    }
