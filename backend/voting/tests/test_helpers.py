import pytest
import respx
from django.conf import settings
from pythonit_toolkit.pastaporto.entities import Pastaporto, PastaportoUserInfo

from voting.helpers import pastaporto_user_info_can_vote

pytestmark = pytest.mark.django_db


def _get_pastaporto(user) -> Pastaporto:
    return Pastaporto(
        PastaportoUserInfo.from_data(
            {"id": user.id, "email": user.email, "is_staff": user.is_staff}
        )
    )


def test_normal_user_cannot_vote(submission_factory, user, mocker):
    submission = submission_factory()
    pastaporto = _get_pastaporto(user)
    mocker.patch("voting.helpers.user_has_admission_ticket", return_value=False)

    with respx.mock as mock:
        mock.post(f"{settings.ASSOCIATION_BACKEND_SERVICE}/internal-api").respond(
            json={"data": {"userIdIsMember": False}}
        )
        assert pastaporto_user_info_can_vote(pastaporto, submission.conference) is False


def test_user_can_vote_if_has_sent_a_submission(submission_factory, user):
    submission = submission_factory(speaker_id=user.id)
    pastaporto = _get_pastaporto(user)

    assert pastaporto_user_info_can_vote(pastaporto, submission.conference) is True


def test_user_can_vote_if_has_bought_a_ticket_for_this_edition(
    conference, user, mocker
):
    pastaporto = _get_pastaporto(user)
    admission_ticket_mock = mocker.patch(
        "voting.helpers.user_has_admission_ticket", return_value=True
    )

    assert pastaporto_user_info_can_vote(pastaporto, conference) is True
    admission_ticket_mock.assert_called()


def test_user_can_vote_if_is_a_admin(admin_user, conference, mocker):
    pastaporto = _get_pastaporto(admin_user)
    mocker.patch("voting.helpers.user_has_admission_ticket", return_value=False)

    assert pastaporto_user_info_can_vote(pastaporto, conference) is True


@pytest.mark.parametrize("is_member", (True, False))
def test_user_can_vote_if_is_a_member_of_python_italia(
    user, conference, mocker, is_member
):
    pastaporto = _get_pastaporto(user)
    mocker.patch("voting.helpers.user_has_admission_ticket", return_value=False)

    with respx.mock as mock:
        mock.post(f"{settings.ASSOCIATION_BACKEND_SERVICE}/internal-api").respond(
            json={"data": {"userIdIsMember": is_member}}
        )
        assert pastaporto_user_info_can_vote(pastaporto, conference) == is_member


def test_user_can_vote_if_has_ticket_for_a_previous_conference(
    user, conference, mocker, included_event_factory
):
    def side_effect(email, event_organizer, event_slug, additional_events):
        return (
            additional_events[0]["organizer_slug"] == "organizer-slug"
            and additional_events[0]["event_slug"] == "event-slug"
        )

    pastaporto = _get_pastaporto(user)
    mocker.patch("voting.helpers.user_has_admission_ticket", side_effect=side_effect)
    included_event_factory(
        conference=conference,
        pretix_organizer_id="organizer-slug",
        pretix_event_id="event-slug",
    )

    with respx.mock as mock:
        mock.post(f"{settings.ASSOCIATION_BACKEND_SERVICE}/internal-api").respond(
            json={"data": {"userIdIsMember": False}}
        )

        assert pastaporto_user_info_can_vote(pastaporto, conference) is True
