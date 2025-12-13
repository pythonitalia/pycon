from decimal import Decimal

import pytest

from grants.tests.factories import (
    GrantFactory,
    GrantReimbursementFactory,
)
from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory
from users.tests.factories import UserFactory
from visa.models import InvitationLetterRequestOnBehalfOf
from visa.tests.factories import InvitationLetterRequestFactory

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
    assert request.has_grant is False

    # With matching user, it is found
    user = UserFactory(email="example@example.org")
    assert request.user.id == user.id


@pytest.mark.parametrize(
    "categories,expected_has_accommodation,expected_has_travel,expected_type",
    [
        (["ticket", "accommodation"], True, False, "accommodation_ticket"),
        (["ticket"], False, False, "ticket"),
        (["ticket", "travel"], False, True, "ticket_travel"),
        (
            ["ticket", "travel", "accommodation"],
            True,
            True,
            "accommodation_ticket_travel",
        ),
    ],
)
def test_request_grant_info(
    categories, expected_has_accommodation, expected_has_travel, expected_type
):
    request = InvitationLetterRequestFactory(
        on_behalf_of=InvitationLetterRequestOnBehalfOf.SELF,
        email_address="example@example.org",
    )
    grant = GrantFactory(
        conference=request.conference,
        user=request.requester,
    )

    # Create reimbursements based on categories
    if "ticket" in categories:
        GrantReimbursementFactory(
            grant=grant,
            category__conference=request.conference,
            category__ticket=True,
            granted_amount=Decimal("100"),
        )
    if "travel" in categories:
        GrantReimbursementFactory(
            grant=grant,
            category__conference=request.conference,
            category__travel=True,
            granted_amount=Decimal("500"),
        )
    if "accommodation" in categories:
        GrantReimbursementFactory(
            grant=grant,
            category__conference=request.conference,
            category__accommodation=True,
            granted_amount=Decimal("200"),
        )

    assert request.user_grant == grant
    assert request.has_grant is True
    assert request.has_accommodation_via_grant() == expected_has_accommodation
    assert request.has_travel_via_grant() == expected_has_travel
    # grant_approved_type returns sorted categories joined by underscore
    assert request.grant_approved_type == expected_type


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


def test_send_via_email(django_capture_on_commit_callbacks, mocker):
    mock_task = mocker.patch("visa.tasks.send_invitation_letter_via_email")
    request = InvitationLetterRequestFactory(
        on_behalf_of=InvitationLetterRequestOnBehalfOf.SELF,
    )

    with django_capture_on_commit_callbacks(execute=True):
        request.send_via_email()

    mock_task.delay.assert_called_once_with(invitation_letter_request_id=request.id)
