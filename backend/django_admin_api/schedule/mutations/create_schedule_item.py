from custom_admin.audit import create_addition_admin_log_entry
from django.db import transaction
from languages.models import Language

import strawberry
from schedule.models import ScheduleItem as ScheduleItemModel, Slot as SlotModel
from django_admin_api.schedule.types.slot import Slot
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


@strawberry.field
def create_schedule_item(info: Info, input: CreateScheduleItemInput) -> Slot:
    slot = SlotModel.objects.for_conference(input.conference_id).get(id=input.slot_id)

    best_language = get_best_language(input.language_id, input.proposal_id)

    with transaction.atomic():
        schedule_item = ScheduleItemModel.objects.create(
            conference_id=input.conference_id,
            type=input.type,
            submission_id=input.proposal_id,
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
    return Slot.from_model(slot)


def get_best_language(language_id, proposal_id):
    if language_id:
        return language_id

    if proposal_id:
        proposal_first_language = Submission.objects.get(
            id=proposal_id
        ).languages.first()
        return proposal_first_language.id

    english_language = Language.objects.get(code="en")
    return english_language.id
