import typing
from datetime import date, datetime, time, timedelta

import strawberry
from django.db import transaction
from strawberry import ID

from api.conferences.types import Day, ScheduleSlot
from api.helpers.ids import decode_hashid
from api.schedule.types import ScheduleInvitation, ScheduleInvitationOption
from api.schedule.types import ScheduleItem as ScheduleItemType
from api.submissions.permissions import IsSubmissionSpeakerOrStaff
from conferences.models import Conference
from domain_events.publisher import send_new_schedule_invitation_answer
from languages.models import Language
from pretix.db import user_has_admission_ticket
from schedule.models import Day as DayModel
from schedule.models import ScheduleItem, ScheduleItemAttendee, Slot
from submissions.models import Submission

from ..permissions import IsAuthenticated, IsStaffPermission


@strawberry.type
class AddScheduleSlotError:
    message: str


def add_minutes_to_time(time: time, minutes: int) -> time:
    return (datetime.combine(date(1, 1, 1), time) + timedelta(minutes=minutes)).time()


@strawberry.type
class UpdateOrCreateSlotItemError:
    message: str


@strawberry.input
class UpdateOrCreateSlotItemInput:
    slot_id: strawberry.ID
    rooms: typing.List[strawberry.ID]
    title: typing.Optional[str] = None
    item_id: typing.Optional[strawberry.ID] = None
    keynote_id: typing.Optional[strawberry.ID] = None
    submission_id: typing.Optional[strawberry.ID] = None

    def get_schedule_item_type(self):
        if self.keynote_id:
            return ScheduleItem.TYPES.keynote

        if self.submission_id:
            return ScheduleItem.TYPES.submission

        return ScheduleItem.TYPES.custom


@strawberry.type
class UpdateOrCreateSlotItemResult:
    updated_slots: typing.List[ScheduleSlot]


@strawberry.input
class UpdateScheduleInvitationInput:
    submission_id: strawberry.ID
    option: ScheduleInvitationOption
    notes: str


@strawberry.type
class ScheduleInvitationNotFound:
    message: str = "Invitation not found"


@strawberry.type
class UserIsAlreadyBooked:
    message: str = "You are already booked for this event"


@strawberry.type
class UserIsNotBooked:
    message: str = "You are not booked for this event"


@strawberry.type
class ScheduleItemNotBookable:
    message: str = "This event does not require booking"


@strawberry.type
class UserNeedsConferenceTicket:
    message: str = "You need to buy a ticket"


@strawberry.type
class ScheduleItemIsFull:
    message: str = "This event is full"


BookSpotScheduleItemResult = strawberry.union(
    "BookSpotScheduleItemResult",
    (
        ScheduleItemType,
        ScheduleItemIsFull,
        UserNeedsConferenceTicket,
        UserIsAlreadyBooked,
        ScheduleItemNotBookable,
    ),
)

CancelSpotScheduleItemResult = strawberry.union(
    "CancelSpotScheduleItemResult",
    (ScheduleItemType, UserIsNotBooked, ScheduleItemNotBookable),
)


@strawberry.type
class ScheduleMutations:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def book_spot_schedule_item(self, info, id: ID) -> BookSpotScheduleItemResult:
        schedule_item = ScheduleItem.objects.get(id=id)
        user_id = info.context.request.user.id

        if not user_has_admission_ticket(
            email=info.context.request.user.email,
            event_organizer=schedule_item.conference.pretix_organizer_id,
            event_slug=schedule_item.conference.pretix_event_id,
        ):
            return UserNeedsConferenceTicket()

        if schedule_item.attendees_total_capacity is None:
            return ScheduleItemNotBookable()

        if schedule_item.attendees.filter(user_id=user_id).exists():
            return UserIsAlreadyBooked()

        if schedule_item.attendees.count() >= schedule_item.attendees_total_capacity:
            return ScheduleItemIsFull()

        ScheduleItemAttendee.objects.create(
            schedule_item=schedule_item, user_id=user_id
        )
        schedule_item._type_definition = ScheduleItemType._type_definition
        return schedule_item

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def cancel_booking_schedule_item(
        self, info, id: ID
    ) -> CancelSpotScheduleItemResult:
        schedule_item = ScheduleItem.objects.get(id=id)
        user_id = info.context.request.user.id

        if schedule_item.attendees_total_capacity is None:
            return ScheduleItemNotBookable()

        if not schedule_item.attendees.filter(user_id=user_id).exists():
            return UserIsNotBooked()

        ScheduleItemAttendee.objects.filter(
            schedule_item=schedule_item, user_id=user_id
        ).delete()
        schedule_item._type_definition = ScheduleItemType._type_definition
        return schedule_item

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_schedule_invitation(
        self, info, input: UpdateScheduleInvitationInput
    ) -> typing.Union[ScheduleInvitationNotFound, ScheduleInvitation]:
        submission = Submission.objects.get_by_hashid(input.submission_id)

        if not IsSubmissionSpeakerOrStaff().has_object_permission(info, submission):
            return ScheduleInvitationNotFound()

        # TODO We assume here that a submission can only be in one schedule item
        # since currently we do not schedule the same talk to appear multiple times
        # in the future this needs to be fixed :)
        schedule_item = (
            ScheduleItem.objects.filter(
                submission_id=submission.id,
                conference_id=submission.conference_id,
            )
            .exclude(status=ScheduleItem.STATUS.cancelled)
            .first()
        )

        if not schedule_item:
            return ScheduleInvitationNotFound()

        new_status = input.option.to_schedule_item_status()
        new_notes = input.notes

        if (
            schedule_item.status == new_status
            and schedule_item.speaker_invitation_notes == new_notes
        ):
            # If nothing changed, do nothing
            return ScheduleInvitation.from_django_model(schedule_item)

        with transaction.atomic():
            schedule_item.status = new_status
            schedule_item.speaker_invitation_notes = new_notes
            schedule_item.save()

        send_new_schedule_invitation_answer(
            schedule_item=schedule_item, request=info.context.request
        )
        return ScheduleInvitation.from_django_model(schedule_item)

    @strawberry.mutation(permission_classes=[IsStaffPermission])
    def add_schedule_slot(
        self, info, conference: strawberry.ID, duration: int, day: date
    ) -> typing.Union[AddScheduleSlotError, Day]:
        conference = Conference.objects.get(code=conference)
        day, _ = DayModel.objects.get_or_create(day=day, conference=conference)

        last_slot = day.slots.last()

        hour = (
            add_minutes_to_time(last_slot.hour, last_slot.duration)
            if last_slot
            else time(8, 30)
        )

        Slot.objects.create(day=day, hour=hour, duration=duration)

        return Day.from_db(day)

    @strawberry.mutation(permission_classes=[IsStaffPermission])
    def update_or_create_slot_item(
        self, info, input: UpdateOrCreateSlotItemInput
    ) -> typing.Union[UpdateOrCreateSlotItemError, UpdateOrCreateSlotItemResult]:
        # TODO: validate this is not none
        slot = Slot.objects.select_related("day").filter(id=input.slot_id).first()

        keynote_id = input.keynote_id
        submission_id = (
            decode_hashid(input.submission_id) if input.submission_id else None
        )

        data = {
            "type": input.get_schedule_item_type(),
            "slot": slot,
            "submission_id": submission_id,
            "keynote_id": keynote_id,
            "conference": slot.day.conference,
        }

        if input.title:
            data["title"] = input.title

        updated_slots: typing.List[ScheduleSlot] = []

        if input.item_id:
            schedule_item = ScheduleItem.objects.select_related("slot").get(
                id=input.item_id
            )
            updated_slots.append(
                ScheduleSlot(
                    hour=schedule_item.slot.hour,
                    duration=schedule_item.slot.duration,
                    id=schedule_item.slot.id,
                )
            )

            # make sure we keep the same type and submission
            data["submission_id"] = schedule_item.submission_id
            data["keynote_id"] = schedule_item.keynote_id
            data["type"] = schedule_item.type

            ScheduleItem.objects.filter(id=input.item_id).update(**data)
        else:
            language_code = "en"

            if submission_id:
                language_code = (
                    Submission.objects.filter(id=submission_id)
                    .values_list("languages__code", flat=True)
                    .order_by("languages__code")
                    .first()
                )

            data["language"] = Language.objects.get(code=language_code)

            schedule_item = ScheduleItem.objects.create(**data)

        schedule_item.rooms.set(input.rooms)

        updated_slots.append(
            ScheduleSlot(hour=slot.hour, duration=slot.duration, id=slot.id)
        )

        return UpdateOrCreateSlotItemResult(updated_slots=updated_slots)
