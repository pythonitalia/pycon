from datetime import date, time

from pytest import mark

from conferences.tests.factories import ConferenceFactory, DurationFactory
from i18n.strings import LazyI18nString
from schedule import models
from schedule.tests.factories import DayFactory, ScheduleItemFactory, SlotFactory
from submissions.tests.factories import SubmissionFactory

SCHEDULE_INVITATION_QUERY = """
    query GetScheduleInvitation($submissionId: ID!, $language: String!) {
      scheduleInvitation(submissionId: $submissionId) {
        id
        option
        notes
        title
        submission {
          id
          title(language: $language)
          duration {
            id
            duration
          }
        }
        dates {
          id
          start
          end
          duration
        }
      }
    }
"""


@mark.django_db
def test_schedule_invitation_frontend_query(
    graphql_client,
    user,
    django_assert_num_queries,
):
    conference = ConferenceFactory()
    duration = DurationFactory(conference=conference, duration=45)
    submission = SubmissionFactory(
        conference=conference,
        duration=duration,
        speaker=user,
        title=LazyI18nString({"en": "Frontend title"}),
    )
    schedule_item = ScheduleItemFactory(
        conference=conference,
        duration=None,
        speaker_invitation_notes="Bring a laptop",
        status=models.ScheduleItem.STATUS.confirmed,
        submission=submission,
        title="Schedule title",
        type=models.ScheduleItem.TYPES.talk,
        slot=SlotFactory(
            day=DayFactory(conference=conference, day=date(2026, 5, 21)),
            duration=30,
            hour=time(10, 15),
        ),
    )
    graphql_client.force_login(user)

    with django_assert_num_queries(4):
        response = graphql_client.query(
            SCHEDULE_INVITATION_QUERY,
            variables={"language": "en", "submissionId": submission.hashid},
        )

    assert "errors" not in response
    assert response["data"]["scheduleInvitation"] == {
        "id": submission.hashid,
        "option": "CONFIRM",
        "notes": "Bring a laptop",
        "title": "Schedule title",
        "submission": {
            "id": submission.hashid,
            "title": "Frontend title",
            "duration": {
                "id": str(duration.id),
                "duration": 45,
            },
        },
        "dates": [
            {
                "id": str(schedule_item.id),
                "start": "2026-05-21T10:15:00",
                "end": "2026-05-21T10:45:00",
                "duration": 30,
            }
        ],
    }
