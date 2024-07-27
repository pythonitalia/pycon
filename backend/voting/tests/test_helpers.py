from association_membership.tests.factories import (
    MembershipFactory,
)
from voting.tests.factories.included_event import IncludedEventFactory
from conferences.tests.factories import ConferenceFactory
from submissions.tests.factories import SubmissionFactory
import pytest
from association_membership.enums import MembershipStatus

from voting.helpers import check_if_user_can_vote

pytestmark = pytest.mark.django_db


def test_normal_user_cannot_vote(user, mocker):
    submission = SubmissionFactory()
    mocker.patch("voting.helpers.user_has_admission_ticket", return_value=False)

    assert check_if_user_can_vote(user, submission.conference) is False


def test_user_can_vote_if_has_sent_a_submission(user):
    submission = SubmissionFactory(speaker_id=user.id)

    assert check_if_user_can_vote(user, submission.conference) is True


def test_user_can_vote_if_has_bought_a_ticket_for_this_edition(user, mocker):
    conference = ConferenceFactory()

    admission_ticket_mock = mocker.patch(
        "voting.helpers.user_has_admission_ticket", return_value=True
    )

    assert check_if_user_can_vote(user, conference) is True
    admission_ticket_mock.assert_called()


def test_user_can_vote_if_is_a_admin(admin_user, mocker):
    conference = ConferenceFactory()

    mocker.patch("voting.helpers.user_has_admission_ticket", return_value=False)

    assert check_if_user_can_vote(admin_user, conference) is True


@pytest.mark.parametrize("is_member", (True, False))
def test_user_can_vote_if_is_a_member_of_python_italia(user, mocker, is_member):
    conference = ConferenceFactory()

    mocker.patch("voting.helpers.user_has_admission_ticket", return_value=False)
    MembershipFactory(
        user=user,
        status=MembershipStatus.ACTIVE if is_member else MembershipStatus.PENDING,
    )

    assert check_if_user_can_vote(user, conference) == is_member


def test_user_can_vote_if_has_ticket_for_a_previous_conference(user, mocker):
    conference = ConferenceFactory()

    def side_effect(email, event_organizer, event_slug, additional_events):
        return (
            additional_events[0]["organizer_slug"] == "organizer-slug"
            and additional_events[0]["event_slug"] == "event-slug"
        )

    mocker.patch("voting.helpers.user_has_admission_ticket", side_effect=side_effect)
    IncludedEventFactory(
        conference=conference,
        pretix_organizer_id="organizer-slug",
        pretix_event_id="event-slug",
    )

    assert check_if_user_can_vote(user, conference) is True
