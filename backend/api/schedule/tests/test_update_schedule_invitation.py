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
    submission_factory,
    graphql_client,
    user,
    schedule_item_factory,
    slot_factory,
    day_factory,
    option,
    expected_status,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )

    graphql_client.force_login(user)
    submission = submission_factory(
        speaker_id=user.id,
    )

    schedule_item = schedule_item_factory(
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(conference=submission.conference), hour="10:00", duration=30
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


def test_saving_the_same_answer_does_not_trigger_event(
    submission_factory,
    graphql_client,
    user,
    schedule_item_factory,
    slot_factory,
    day_factory,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )

    graphql_client.force_login(user)
    submission = submission_factory(
        speaker_id=user.id,
    )

    schedule_item = schedule_item_factory(
        status=ScheduleItem.STATUS.confirmed,
        speaker_invitation_notes="notes",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(conference=submission.conference), hour="10:00", duration=30
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


def test_changing_notes_triggers_a_new_event(
    submission_factory,
    graphql_client,
    user,
    schedule_item_factory,
    slot_factory,
    day_factory,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )

    graphql_client.force_login(user)
    submission = submission_factory(
        speaker_id=user.id,
    )

    schedule_item = schedule_item_factory(
        status=ScheduleItem.STATUS.confirmed,
        speaker_invitation_notes="notes",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(conference=submission.conference), hour="10:00", duration=30
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


def test_random_user_cannot_update_an_invitation(
    submission_factory,
    graphql_client,
    user,
    schedule_item_factory,
    slot_factory,
    day_factory,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )

    graphql_client.force_login(user)
    submission = submission_factory()

    schedule_item = schedule_item_factory(
        status=ScheduleItem.STATUS.waiting_confirmation,
        speaker_invitation_notes="",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(conference=submission.conference), hour="10:00", duration=30
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
    submission_factory, graphql_client, user, mocker
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )

    graphql_client.force_login(user)
    submission = submission_factory(
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


def test_reqires_authentication(
    submission_factory,
    graphql_client,
    schedule_item_factory,
    slot_factory,
    day_factory,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )

    submission = submission_factory()

    schedule_item = schedule_item_factory(
        status=ScheduleItem.STATUS.waiting_confirmation,
        speaker_invitation_notes="",
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(conference=submission.conference), hour="10:00", duration=30
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
    submission_factory,
    graphql_client,
    admin_user,
    schedule_item_factory,
    slot_factory,
    day_factory,
    mocker,
):
    mock_event = mocker.patch(
        "api.schedule.mutations.update_schedule_invitation.notify_new_schedule_invitation_answer_slack"
    )

    graphql_client.force_login(admin_user)
    submission = submission_factory()

    schedule_item = schedule_item_factory(
        submission=submission,
        type=ScheduleItem.TYPES.submission,
        conference=submission.conference,
        slot=slot_factory(
            day=day_factory(conference=submission.conference), hour="10:00", duration=30
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
