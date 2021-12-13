import pytest
from pythonit_toolkit.pastaporto.entities import Pastaporto, PastaportoUserInfo

from voting.helpers import pastaporto_user_info_can_vote


def _get_pastaporto(user) -> Pastaporto:
    return Pastaporto(
        PastaportoUserInfo.from_data(
            {"id": user.id, "email": user.email, "isStaff": False}
        )
    )


@pytest.mark.django_db
def test_user_can_vote_if_has_sent_a_submission(submission_factory, user):
    submission = submission_factory(speaker_id=user.id)
    pastaporto = _get_pastaporto(user)

    assert pastaporto_user_info_can_vote(pastaporto, submission.conference) is True


@pytest.mark.django_db
def test_user_can_vote_if_has_bought_a_ticket_for_this_edition(
    conference, user, mocker
):
    pastaporto = _get_pastaporto(user)
    admission_ticket_mock = mocker.patch(
        "voting.helpers.user_has_admission_ticket", return_value=True
    )

    assert pastaporto_user_info_can_vote(pastaporto, conference) is True
    admission_ticket_mock.assert_called()


@pytest.mark.django_db
def test_user_can_vote_if_is_a_admin(admin_user, conference):
    pastaporto = _get_pastaporto(admin_user)

    assert pastaporto_user_info_can_vote(pastaporto, conference) is True
