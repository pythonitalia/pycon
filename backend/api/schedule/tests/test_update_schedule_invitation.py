from submissions.tests.factories import SubmissionFactory
from schedule.tests.factories import DayFactory, ScheduleItemFactory, SlotFactory
from pytest import mark

from schedule.models import ScheduleItem

pytestmark = mark.django_db


@mark.parametrize(
    "option,expected_status",
    (
        ("CONFIRM", ScheduleItem.STATUS.confirmed),
        ("MAYBE", ScheduleItem.STATUS.maybe),
        ("REJECT", ScheduleItem.STATUS.rejected),
        ("CANT_ATTEND", ScheduleItem.STATUS.cant_attend),
    ),
)
def test_update_invitation_answer(
    graphql_client,
    user,
    option,
    expected_status,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )
    mock_plain = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.send_schedule_invitation_plain_message"
    )

    graphql_client.force_login(user)
    submission = SubmissionFactory(
        speaker_id=user.id,
    )

    schedule_item = ScheduleItemFactory(
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=SlotFactory(
            day=DayFactory(conference=submission.conference), hour="10:00", duration=30
        ),
    )

    response = graphql_client.query(
        """mutation($input: UpdateScheduleInvitationInput!) {
        updateScheduleInvitation(input: $input) {
            __typename
            ... on ScheduleInvitation {
                option
                notes
            }
        }
    }""",
        variables={
            "input": {
                "submissionId": submission.hashid,
                "option": option,
                "notes": "notes",
            }
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateScheduleInvitation"] == {
        "__typename": "ScheduleInvitation",
        "option": option,
        "notes": "notes",
    }

    schedule_item.refresh_from_db()
    assert schedule_item.status == expected_status
    assert schedule_item.speaker_invitation_notes == "notes"

    mock_event.delay.assert_called_once()
    mock_plain.delay.assert_called_once_with(
        schedule_item_id=schedule_item.id,
        message="notes",
    )


def test_saving_the_same_answer_does_not_trigger_event(
    graphql_client,
    user,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )
    mock_plain = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.send_schedule_invitation_plain_message"
    )

    graphql_client.force_login(user)
    submission = SubmissionFactory(
        speaker_id=user.id,
    )

    schedule_item = ScheduleItemFactory(
        status=ScheduleItem.STATUS.confirmed,
        speaker_invitation_notes="notes",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=SlotFactory(
            day=DayFactory(conference=submission.conference), hour="10:00", duration=30
        ),
    )

    response = graphql_client.query(
        """mutation($input: UpdateScheduleInvitationInput!) {
        updateScheduleInvitation(input: $input) {
            __typename
            ... on ScheduleInvitation {
                option
                notes
            }
        }
    }""",
        variables={
            "input": {
                "submissionId": submission.hashid,
                "option": "CONFIRM",
                "notes": "notes",
            }
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateScheduleInvitation"] == {
        "__typename": "ScheduleInvitation",
        "option": "CONFIRM",
        "notes": "notes",
    }

    schedule_item.refresh_from_db()
    assert schedule_item.status == ScheduleItem.STATUS.confirmed
    assert schedule_item.speaker_invitation_notes == "notes"

    mock_event.delay.assert_not_called()
    mock_plain.delay.assert_not_called()


def test_changing_notes_triggers_a_new_event(
    graphql_client,
    user,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )
    mock_plain = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.send_schedule_invitation_plain_message"
    )

    graphql_client.force_login(user)
    submission = SubmissionFactory(
        speaker_id=user.id,
    )

    schedule_item = ScheduleItemFactory(
        status=ScheduleItem.STATUS.confirmed,
        speaker_invitation_notes="notes",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=SlotFactory(
            day=DayFactory(conference=submission.conference), hour="10:00", duration=30
        ),
    )

    response = graphql_client.query(
        """mutation($input: UpdateScheduleInvitationInput!) {
        updateScheduleInvitation(input: $input) {
            __typename
            ... on ScheduleInvitation {
                option
                notes
            }
        }
    }""",
        variables={
            "input": {
                "submissionId": submission.hashid,
                "option": "CONFIRM",
                "notes": "newnotes",
            }
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateScheduleInvitation"] == {
        "__typename": "ScheduleInvitation",
        "option": "CONFIRM",
        "notes": "newnotes",
    }

    schedule_item.refresh_from_db()
    assert schedule_item.status == ScheduleItem.STATUS.confirmed
    assert schedule_item.speaker_invitation_notes == "newnotes"

    mock_event.delay.assert_called()
    mock_plain.delay.assert_called_once_with(
        schedule_item_id=schedule_item.id,
        message="newnotes",
    )


def test_random_user_cannot_update_an_invitation(
    graphql_client,
    user,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )

    graphql_client.force_login(user)
    submission = SubmissionFactory()

    schedule_item = ScheduleItemFactory(
        status=ScheduleItem.STATUS.waiting_confirmation,
        speaker_invitation_notes="",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=SlotFactory(
            day=DayFactory(conference=submission.conference), hour="10:00", duration=30
        ),
    )

    response = graphql_client.query(
        """mutation($input: UpdateScheduleInvitationInput!) {
        updateScheduleInvitation(input: $input) {
            __typename
        }
    }""",
        variables={
            "input": {
                "submissionId": submission.hashid,
                "option": "CONFIRM",
                "notes": "newnotes",
            }
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateScheduleInvitation"] == {
        "__typename": "ScheduleInvitationNotFound",
    }

    schedule_item.refresh_from_db()
    assert schedule_item.status == ScheduleItem.STATUS.waiting_confirmation
    assert schedule_item.speaker_invitation_notes == ""

    mock_event.delay.assert_not_called()


def test_cannot_update_schedule_if_submission_doesnt_have_a_matching_schedule(
    graphql_client, user, mocker
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )

    graphql_client.force_login(user)
    submission = SubmissionFactory(
        speaker_id=user.id,
    )

    response = graphql_client.query(
        """mutation($input: UpdateScheduleInvitationInput!) {
        updateScheduleInvitation(input: $input) {
            __typename
        }
    }""",
        variables={
            "input": {
                "submissionId": submission.hashid,
                "option": "CONFIRM",
                "notes": "newnotes",
            }
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateScheduleInvitation"] == {
        "__typename": "ScheduleInvitationNotFound",
    }

    mock_event.delay.assert_not_called()


def test_requires_authentication(
    graphql_client,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )

    submission = SubmissionFactory()

    schedule_item = ScheduleItemFactory(
        status=ScheduleItem.STATUS.waiting_confirmation,
        speaker_invitation_notes="",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=SlotFactory(
            day=DayFactory(conference=submission.conference), hour="10:00", duration=30
        ),
    )

    response = graphql_client.query(
        """mutation($input: UpdateScheduleInvitationInput!) {
        updateScheduleInvitation(input: $input) {
            __typename
        }
    }""",
        variables={
            "input": {
                "submissionId": submission.hashid,
                "option": "CONFIRM",
                "notes": "newnotes",
            }
        },
    )

    assert response["errors"][0]["message"] == "User not logged in"
    assert not response.get("data")

    schedule_item.refresh_from_db()
    assert schedule_item.status == ScheduleItem.STATUS.waiting_confirmation
    assert schedule_item.speaker_invitation_notes == ""

    mock_event.delay.assert_not_called()


def test_staff_can_update_invitation_answer(
    graphql_client,
    admin_user,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )
    mock_plain = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.send_schedule_invitation_plain_message"
    )

    graphql_client.force_login(admin_user)
    submission = SubmissionFactory()

    schedule_item = ScheduleItemFactory(
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=SlotFactory(
            day=DayFactory(conference=submission.conference), hour="10:00", duration=30
        ),
    )

    response = graphql_client.query(
        """mutation($input: UpdateScheduleInvitationInput!) {
        updateScheduleInvitation(input: $input) {
            __typename
            ... on ScheduleInvitation {
                option
                notes
            }
        }
    }""",
        variables={
            "input": {
                "submissionId": submission.hashid,
                "option": "CONFIRM",
                "notes": "notes",
            }
        },
    )

    assert not response.get("errors")
    assert response["data"]["updateScheduleInvitation"] == {
        "__typename": "ScheduleInvitation",
        "option": "CONFIRM",
        "notes": "notes",
    }

    schedule_item.refresh_from_db()
    assert schedule_item.status == ScheduleItem.STATUS.confirmed
    assert schedule_item.speaker_invitation_notes == "notes"

    mock_event.delay.assert_called_once()
    mock_plain.delay.assert_called_once_with(
        schedule_item_id=schedule_item.id,
        message="notes",
    )
