import strawberry
from enum import Enum
from typing import Dict, List, Set
import pretix
from conferences.models import Conference
from schedule.models import ScheduleItem
from django.core.cache import cache
from badges.models import AttendeeConferenceRole
from django.db.models import Q


class Role(Enum):
    ATTENDEE = "attendee"
    STAFF = "staff"
    SPEAKER = "speaker"
    SPONSOR = "sponsor"
    KEYNOTER = "keynoter"

    @staticmethod
    def choices():
        return ((role.value, role.name) for role in Role)


ConferenceRole = strawberry.enum(Role, name="ConferenceRole")

ROLES_PRIORITY = [
    Role.STAFF,
    Role.SPEAKER,
    Role.KEYNOTER,
    Role.SPONSOR,
    Role.ATTENDEE,
]


def speakers_user_ids(conference: Conference) -> Set[int]:
    cache_key = f"conference:{conference.id}:speakers_user_ids"

    if cache.has_key(cache_key):
        return cache.get(cache_key)

    submission_speakers = list(
        ScheduleItem.objects.filter(
            conference=conference,
        )
        .values_list(
            "submission__speaker_id",
            flat=True,
        )
        .distinct()
    )
    additional_speakers = list(
        ScheduleItem.objects.filter(conference=conference)
        .values_list("additional_speakers__user_id", flat=True)
        .distinct()
    )
    items = set(submission_speakers + additional_speakers)
    cache.set(cache_key, items, timeout=60 * 60 * 24 * 2)
    return items


def get_conference_roles_for_ticket_data(
    conference: Conference, user_id: int, data: Dict
) -> List[Role]:
    return _get_roles(
        conference=conference,
        user_id=user_id,
        ticket=data,
    )


def get_conference_roles_for_user(
    conference: Conference, user_id: int, user_email: str
) -> List[Role]:
    user_tickets = pretix.get_user_tickets(conference, user_email)
    admission_tickets = [
        user_ticket
        for user_ticket in user_tickets
        if user_ticket["item"]["admission"]
        and user_ticket["attendee_email"] == user_email
    ]

    if not admission_tickets:
        # no matching tickets
        return []

    return _get_roles(
        conference=conference,
        user_id=user_id,
        ticket=admission_tickets[0],
    )


def _get_roles(conference: Conference, user_id: int, ticket: dict) -> List[Role]:
    ticket_id = ticket["id"]

    # check if we have overrides for this ticket / user
    manual_role = AttendeeConferenceRole.objects.filter(
        Q(order_position_id=ticket_id) | Q(user_id=user_id),
        conference=conference,
    ).first()

    roles = (
        manual_role.roles
        if manual_role
        else _calculate_roles(conference, user_id, ticket)
    )
    return sorted(
        roles,
        key=lambda role: ROLES_PRIORITY.index(Role(role)),
    )


def _calculate_roles(conference: Conference, user_id: int, ticket: dict) -> List[Role]:
    roles = [
        Role.ATTENDEE,
    ]

    vouchers = pretix.get_all_vouchers(conference)

    if (voucher_id := ticket["voucher"]) and (voucher := vouchers.get(voucher_id)):
        tags = voucher["tag"].lower().split(",")
        voucher_code = voucher["code"].lower()

        if voucher_code.startswith("staff-") or "staff" in tags:
            roles.append(Role.STAFF)

        if voucher_code.startswith("keynoter-") or "keynoter" in tags:
            roles.append(Role.KEYNOTER)

        if "sponsor" in tags:
            roles.append(Role.SPONSOR)

        if "speakers" in tags:
            roles.append(Role.SPEAKER)

    # We do not know if they are a speaker via voucher code
    # so we check if there is a schedule item where they are a speaker
    # this has the effect of tagging non-speakers as speakers if their ticket
    # was purchased by a speaker (I know only one case of this happening right now)
    user_is_in_schedule_item = user_id in speakers_user_ids(conference)
    if Role.SPEAKER not in roles and user_is_in_schedule_item:
        roles.append(Role.SPEAKER)

    return roles
