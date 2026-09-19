from datetime import date, time

import pytest

from conferences.tests.factories import (
    AudienceLevelFactory,
    ConferenceFactory,
    DurationFactory,
    KeynoteFactory,
    KeynoteSpeakerFactory,
)
from files_upload.tests.factories import ParticipantAvatarFileFactory
from participants.tests.factories import ParticipantFactory
from schedule.models import DayRoomThroughModel
from schedule.tests.factories import (
    DayFactory,
    RoomFactory,
    ScheduleItemAdditionalSpeakerFactory,
    ScheduleItemFactory,
    SlotFactory,
)
from submissions.tests.factories import SubmissionFactory, SubmissionTypeFactory

SCHEDULE_QUERY = """
query Schedule($code: String!, $language: String!) {
  conference(code: $code) {
    id
    timezone
    days {
      day
      rooms {
        id
        name
        type
      }
      slots {
        id
        hour
        endHour
        duration
        type
        items {
          id
          title
          slug
          type
          duration
          hasLimitedCapacity
          userHasSpot
          hasSpacesLeft
          spacesLeft
          linkTo
          audienceLevel {
            id
            name
          }
          language {
            id
            name
            code
          }
          submission {
            id
            title(language: $language)
            duration {
              id
              duration
            }
            audienceLevel {
              id
              name
            }
            speaker {
              id
              fullName
            }
            type {
              id
              name
            }
            tags {
              id
              name
            }
          }
          keynote {
            id
            title(language: "en")
            slug(language: "en")
            speakers {
              id
              fullName
            }
          }
          speakers {
            id
            fullname
            participant {
              id
              photo
            }
          }
          rooms {
            id
            name
            type
          }
        }
      }
    }
    audienceLevels {
      id
      name
    }
    durations {
      id
      duration
      allowedSubmissionTypes {
        name
      }
    }
  }
}
"""


@pytest.mark.parametrize("item_count", [1, 4])
@pytest.mark.parametrize(
    ("item_source", "expected_queries"),
    [("submission", 13), ("keynote", 14), ("additional", 13)],
)
@pytest.mark.django_db
def test_frontend_schedule_query_is_constant(
    graphql_client,
    django_assert_num_queries,
    item_count,
    item_source,
    expected_queries,
):
    conference = ConferenceFactory()
    day = DayFactory(conference=conference, day=date(2026, 5, 29))
    room = RoomFactory(name="Main room")
    DayRoomThroughModel.objects.create(day=day, room=room)

    audience_level = AudienceLevelFactory()
    conference.audience_levels.add(audience_level)
    submission_type = SubmissionTypeFactory()
    conference.submission_types.add(submission_type)
    duration = DurationFactory(conference=conference, duration=30)
    duration.allowed_submission_types.add(submission_type)

    for index in range(item_count):
        slot = SlotFactory(day=day, hour=time(9 + index), duration=30)
        if item_source == "submission":
            submission = SubmissionFactory(
                conference=conference,
                audience_level=audience_level,
                duration=duration,
                type=submission_type,
                status="accepted",
                tags=[f"tag-{index}"],
            )
            speaker = submission.speaker
            ScheduleItemFactory(
                conference=conference,
                slot=slot,
                submission=submission,
                type="submission",
                rooms=[room],
                language="en",
            )
        elif item_source == "keynote":
            keynote = KeynoteFactory(conference=conference)
            keynote_speaker = KeynoteSpeakerFactory(keynote=keynote)
            speaker = keynote_speaker.user
            ScheduleItemFactory(
                conference=conference,
                slot=slot,
                submission=None,
                keynote=keynote,
                type="keynote",
                rooms=[room],
                language="en",
            )
        else:
            schedule_item = ScheduleItemFactory(
                conference=conference,
                slot=slot,
                submission=None,
                type="custom",
                rooms=[room],
                language="en",
            )
            additional_speaker = ScheduleItemAdditionalSpeakerFactory(
                scheduleitem=schedule_item
            )
            speaker = additional_speaker.user

        ParticipantFactory(
            conference=conference,
            user=speaker,
            photo_file=ParticipantAvatarFileFactory(uploaded_by=speaker),
        )

    with django_assert_num_queries(expected_queries):
        response = graphql_client.query(
            SCHEDULE_QUERY,
            variables={"code": conference.code, "language": "en"},
        )

    assert "errors" not in response
    items = [
        item
        for slot in response["data"]["conference"]["days"][0]["slots"]
        for item in slot["items"]
    ]
    assert len(items) == item_count
    assert all(item["speakers"][0]["participant"]["photo"] for item in items)
