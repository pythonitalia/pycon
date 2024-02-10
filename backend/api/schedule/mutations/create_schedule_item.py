from custom_admin.audit import create_addition_admin_log_entry
from django.db import transaction
from api.permissions import CanEditSchedule
from languages.models import Language

import strawberry
from schedule.models import ScheduleItem as ScheduleItemModel, Slot as SlotModel
from api.schedule.types.slot import ScheduleSlot
from strawberry.types import Info
from submissions.models import Submission


@strawberry.input
class CreateScheduleItemInput:
    conference_id: strawberry.ID
    type: str
    slot_id: strawberry.ID
    rooms: list[strawberry.ID]
    language_id: strawberry.ID | None = None
    proposal_id: strawberry.ID | None = None
    keynote_id: strawberry.ID | None = None
    title: str | None = ""


@strawberry.field(permission_classes=[CanEditSchedule])
def create_schedule_item(info: Info, input: CreateScheduleItemInput) -> ScheduleSlot:
    slot = SlotModel.objects.for_conference(input.conference_id).get(id=input.slot_id)

    proposal = (
        Submission.objects.get_by_hashid(input.proposal_id)
        if input.proposal_id
        else None
    )
    best_language = get_best_language(input.language_id, proposal)

    with transaction.atomic():
        schedule_item = ScheduleItemModel.objects.create(
            conference_id=input.conference_id,
            type=input.type,
            submission_id=proposal.id if proposal else None,
            keynote_id=input.keynote_id,
            slot=slot,
            language_id=best_language,
            title=input.title,
        )

        schedule_item.rooms.set(input.rooms)

        create_addition_admin_log_entry(
            info.context.request.user,
            schedule_item,
            "Created Schedule Item",
        )
    return slot


def get_best_language(language_id, proposal):
    if language_id:
        return language_id

    if proposal:
        proposal_first_language = proposal.languages.first()
        return proposal_first_language.id

    english_language = Language.objects.get(code="en")
    return english_language.id
