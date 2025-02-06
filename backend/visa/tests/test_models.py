from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory
from grants.models import Grant
from grants.tests.factories import GrantFactory
from users.tests.factories import UserFactory
from visa.models import InvitationLetterRequestOnBehalfOf
from visa.tests.factories import InvitationLetterRequestFactory
import pytest

pytestmark = pytest.mark.django_db


def test_request_on_behalf_of_other():
    request = InvitationLetterRequestFactory(
        on_behalf_of=InvitationLetterRequestOnBehalfOf.OTHER,
        email_address="example@example.org",
    )

    assert request.on_behalf_of_other
    assert request.email == "example@example.org"
    assert request.user is None
    assert request.role == "Attendee"

    # With matching user, it is found
    user = UserFactory(email="example@example.org")
    assert request.user.id == user.id


@pytest.mark.parametrize(
    "approved_type",
    [
        Grant.ApprovedType.ticket_accommodation,
        Grant.ApprovedType.ticket_only,
        Grant.ApprovedType.ticket_travel,
        Grant.ApprovedType.ticket_travel_accommodation,
    ],
)
def test_request_grant_info(approved_type):
    request = InvitationLetterRequestFactory(
        on_behalf_of=InvitationLetterRequestOnBehalfOf.SELF,
        email_address="example@example.org",
    )
    grant = GrantFactory(
        conference=request.conference,
        user=request.requester,
        approved_type=approved_type,
    )

    assert request.user_grant == grant
    assert request.has_accommodation_via_grant() == (
        approved_type
        in [
            Grant.ApprovedType.ticket_accommodation,
            Grant.ApprovedType.ticket_travel_accommodation,
        ]
    )
    assert request.has_travel_via_grant() == (
        approved_type
        in [
            Grant.ApprovedType.ticket_travel,
            Grant.ApprovedType.ticket_travel_accommodation,
        ]
    )
    assert request.grant_approved_type == approved_type


def test_role_for_speakers():
    request = InvitationLetterRequestFactory(
        on_behalf_of=InvitationLetterRequestOnBehalfOf.SELF,
    )
    SubmissionFactory(
        speaker=request.requester,
        conference=request.conference,
        status=Submission.STATUS.accepted,
    )

    assert request.role == "Speaker"


def test_schedule_processing(django_capture_on_commit_callbacks, mocker):
    mock_task = mocker.patch("visa.tasks.process_invitation_letter_request")
    request = InvitationLetterRequestFactory(
        on_behalf_of=InvitationLetterRequestOnBehalfOf.SELF,
    )

    with django_capture_on_commit_callbacks(execute=True):
        request.process()

    mock_task.delay.assert_called_once_with(invitation_letter_request_id=request.id)
