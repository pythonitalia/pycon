import datetime

from pytest import mark

from schedule.models import ScheduleItem

pytestmark = mark.django_db


def test_fetch_an_invitation(
    submission_factory,
    graphql_client,
    user,
    schedule_item_factory,
    slot_factory,
    day_factory,
):
    graphql_client.force_login(user)
    submission = submission_factory(
        speaker_id=user.id,
    )

    schedule_item_factory(
        status=ScheduleItem.STATUS.confirmed,
        speaker_invitation_notes="notes",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(
                day=datetime.date(2020, 10, 10), conference=submission.conference
            ),
            hour=datetime.time(10, 10, 0),
            duration=30,
        ),
    )

    response = graphql_client.query(
        """query($submissionId: ID!) {
        scheduleInvitation(submissionId: $submissionId) {
            option
            notes
            dates {
                start
                end
            }
        }
    }""",
        variables={"submissionId": submission.hashid},
    )

    assert not response.get("errors")
    assert response["data"]["scheduleInvitation"] == {
        "option": "CONFIRM",
        "notes": "notes",
        "dates": [{"start": "2020-10-10T10:10:00", "end": "2020-10-10T10:40:00"}],
    }


def test_random_user_cannot_fetch_the_invite(
    submission_factory,
    graphql_client,
    user,
    schedule_item_factory,
    slot_factory,
    day_factory,
):
    graphql_client.force_login(user)
    submission = submission_factory(
        speaker_id=50000,
    )

    schedule_item_factory(
        status=ScheduleItem.STATUS.confirmed,
        speaker_invitation_notes="notes",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(
                day=datetime.date(2020, 10, 10), conference=submission.conference
            ),
            hour=datetime.time(10, 10, 0),
            duration=30,
        ),
    )

    response = graphql_client.query(
        """query($submissionId: ID!) {
        scheduleInvitation(submissionId: $submissionId) {
            option
            notes
            dates {
                start
                end
            }
        }
    }""",
        variables={"submissionId": submission.hashid},
    )

    assert not response.get("errors")
    assert response["data"]["scheduleInvitation"] is None


def test_staff_can_fetch_the_invite(
    submission_factory,
    graphql_client,
    admin_user,
    schedule_item_factory,
    slot_factory,
    day_factory,
):
    graphql_client.force_login(admin_user)
    submission = submission_factory(
        speaker_id=50000,
    )

    schedule_item_factory(
        status=ScheduleItem.STATUS.confirmed,
        speaker_invitation_notes="notes",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(
                day=datetime.date(2020, 10, 10), conference=submission.conference
            ),
            hour=datetime.time(10, 10, 0),
            duration=30,
        ),
    )

    response = graphql_client.query(
        """query($submissionId: ID!) {
        scheduleInvitation(submissionId: $submissionId) {
            option
            notes
        }
    }""",
        variables={"submissionId": submission.hashid},
    )

    assert not response.get("errors")
    assert response["data"]["scheduleInvitation"] == {
        "option": "CONFIRM",
        "notes": "notes",
    }


def test_requires_authentication(
    submission_factory,
    graphql_client,
    schedule_item_factory,
    slot_factory,
    day_factory,
):
    submission = submission_factory(
        speaker_id=50000,
    )

    schedule_item_factory(
        status=ScheduleItem.STATUS.confirmed,
        speaker_invitation_notes="notes",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(
                day=datetime.date(2020, 10, 10), conference=submission.conference
            ),
            hour=datetime.time(10, 10, 0),
            duration=30,
        ),
    )

    response = graphql_client.query(
        """query($submissionId: ID!) {
        scheduleInvitation(submissionId: $submissionId) {
            option
            notes
            dates {
                start
                end
            }
        }
    }""",
        variables={"submissionId": submission.hashid},
    )

    assert response["errors"][0]["message"] == "User not logged in"
    assert response["data"]["scheduleInvitation"] is None
