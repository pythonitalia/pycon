from django.db import models as django_models
from django.db.models.functions import Coalesce

from api.context import Info
from conferences import models as conference_models
from schedule import models


ATTENDEES_COUNT_ANNOTATION = "graphql_attendees_count"
CAPACITY_ANNOTATION = "graphql_attendees_total_capacity"
USER_HAS_SPOT_ANNOTATION = "graphql_user_has_spot"


def attendees_count_annotation(_info: Info):
    return django_models.Count("attendees", distinct=True)


def capacity_annotation(_info: Info):
    room_capacity = (
        models.Room.objects.filter(talks=django_models.OuterRef("pk"))
        .order_by("pk")
        .values("attendees_total_capacity")[:1]
    )
    return Coalesce(
        "attendees_total_capacity",
        django_models.Subquery(room_capacity),
        output_field=django_models.PositiveIntegerField(),
    )


def user_has_spot_annotation(info: Info):
    user_id = info.context.request.user.id
    if not user_id:
        return django_models.Value(False, output_field=django_models.BooleanField())

    return django_models.Exists(
        models.ScheduleItemAttendee.objects.filter(
            schedule_item_id=django_models.OuterRef("pk"),
            user_id=user_id,
        )
    )


def attendance_annotations(info: Info):
    return {
        ATTENDEES_COUNT_ANNOTATION: attendees_count_annotation(info),
        CAPACITY_ANNOTATION: capacity_annotation(info),
        USER_HAS_SPOT_ANNOTATION: user_has_spot_annotation(info),
    }


def schedule_item_speakers(schedule_item):
    speakers = []

    if schedule_item.submission_id:
        speakers.append(schedule_item.submission.speaker)

    if schedule_item.keynote_id:
        keynote_speakers = getattr(
            schedule_item.keynote,
            "graphql_speakers",
            None,
        )
        if keynote_speakers is None:
            keynote_speakers = schedule_item.keynote.speakers.order_by("id").all()
        speakers.extend(speaker.user for speaker in keynote_speakers)

    additional_speakers = getattr(
        schedule_item,
        "graphql_additional_speakers",
        None,
    )
    if additional_speakers is None:
        additional_speakers = schedule_item.additional_speakers.order_by("id").all()
    speakers.extend(speaker.user for speaker in additional_speakers)

    return [speaker for speaker in speakers if speaker is not None]


def schedule_days_prefetch(info: Info):
    schedule_items = (
        models.ScheduleItem.objects.annotate(
            order=django_models.Case(
                django_models.When(type="custom", then=django_models.Value(1)),
                django_models.When(type="break", then=django_models.Value(1)),
                django_models.When(type="talk", then=django_models.Value(2)),
                django_models.When(type="panel", then=django_models.Value(3)),
                default=django_models.Value(4),
                output_field=django_models.IntegerField(),
            ),
            **attendance_annotations(info),
        )
        .order_by("order")
        .prefetch_related(
            "audience_level",
            "language",
            "rooms",
            django_models.Prefetch(
                "additional_speakers",
                queryset=models.ScheduleItemAdditionalSpeaker.objects.order_by(
                    "id"
                ).select_related("user"),
                to_attr="graphql_additional_speakers",
            ),
            "submission",
            "submission__type",
            "submission__tags",
            "submission__duration",
            "submission__audience_level",
            "submission__speaker",
            "submission__languages",
            "submission__schedule_items",
            "keynote",
            "keynote__schedule_items",
            "keynote__schedule_items__rooms",
            "keynote__schedule_items__slot",
            "keynote__schedule_items__slot__day",
            django_models.Prefetch(
                "keynote__speakers",
                queryset=conference_models.KeynoteSpeaker.objects.order_by(
                    "id"
                ).select_related("user"),
                to_attr="graphql_speakers",
            ),
        )
    )

    return django_models.Prefetch(
        "days",
        queryset=models.Day.objects.order_by("day").prefetch_related(
            "slots",
            "slots__day",
            "slots__day__added_rooms",
            "slots__day__added_rooms__room",
            django_models.Prefetch("slots__items", queryset=schedule_items),
        ),
    )
