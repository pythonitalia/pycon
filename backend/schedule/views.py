import datetime
from conferences.models.conference import Conference
from icalendar import Calendar, Event
from django.http import HttpResponse
from api.helpers.ids import decode_hashid
from django.conf import settings
from pycon.signing import require_signed_request
from schedule.models import ScheduleItem, ScheduleItemStar
from django.views.decorators.http import require_safe
from django.views.decorators.cache import never_cache


@require_safe
@never_cache
@require_signed_request
def user_schedule_item_favourites_calendar(request, conference_id, hash_user_id):
    conference = Conference.objects.get(id=conference_id)
    user_id = decode_hashid(hash_user_id, salt=settings.USER_ID_HASH_SALT, min_length=6)
    starred_schedule_items = ScheduleItem.objects.prefetch_related(
        "submission",
        "keynote",
        "language",
        "slot",
        "rooms",
        "additional_speakers__user",
    ).filter(
        id__in=ScheduleItemStar.objects.for_conference(conference)
        .of_user(user_id)
        .values_list("schedule_item_id", flat=True)
    )

    conference_name = conference.name.localize("en")
    conference_code = conference.code
    conference_timezone = conference.timezone

    utc = datetime.timezone.utc
    now = datetime.datetime.now(utc)

    cal = Calendar()
    cal.add("X-WR-CALNAME", f"{conference_name}'s Schedule")
    cal.add("X-PUBLISHED-TTL", "PT15M")
    cal.add("REFRESH-INTERVAL", "PT15M")
    cal.add("prodid", f"-//{conference_name}//")
    cal.add("version", "2.0")

    for schedule_item in starred_schedule_items:
        event_description = (
            schedule_item.elevator_pitch or schedule_item.abstract
        ).strip() + "\n"
        rooms = ", ".join(schedule_item.rooms.values_list("name", flat=True))
        speakers = [speaker.display_name for speaker in schedule_item.speakers]

        if speakers:
            event_description += f"\nSpeaker(s)/Relatore(i): {', '.join(speakers)}"

        if rooms:
            event_description += f"\nRoom(s)/Stanza(e): {rooms}"

        event_description += (
            f"\nInfo: https://2024.pycon.it/event/{schedule_item.slug}/"
        )

        event = Event()
        event.add("summary", f"[{conference_name}] {schedule_item.title}")
        event.add("location", rooms)
        event.add(
            "description",
            event_description.strip(),
        )
        event.add(
            "uid",
            f"{schedule_item.slug}-{str(schedule_item.start)}-{str(schedule_item.end)}@{conference_code}".replace(
                " ", ""
            ),
        )
        event.add("url", f"https://2024.pycon.it/event/{schedule_item.slug}/")
        event.add(
            "dtstart", conference_timezone.localize(schedule_item.start).astimezone(utc)
        )
        event.add(
            "dtend", conference_timezone.localize(schedule_item.end).astimezone(utc)
        )
        event.add("dtstamp", now)

        cal.add_component(event)

    response = HttpResponse(cal.to_ical(), content_type="text/calendar")
    response["Content-Disposition"] = 'attachment; filename="calendar.ics"'
    return response
