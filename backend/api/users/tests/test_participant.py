import pytest

from api.users.types import User

pytestmark = pytest.mark.django_db


def test_user_participant(user, participant_factory):
    participant = participant_factory(
        user_id=user.id,
        bio="biiiiio",
        photo="https://marcopycontest.blob.core.windows.net/participants-avatars/blob.jpg",
        website="https://google.it",
        twitter_handle="marco",
        speaker_level="intermediate",
        previous_talk_video="",
    )

    user = User.resolve_reference(user.id, user.email)
    participant_type = user.participant(
        info=None, conference=participant.conference.code
    )

    assert participant_type.id == participant.id
    assert participant_type.bio == "biiiiio"
    assert (
        participant_type.photo
        == "https://marcopycontest.blob.core.windows.net/participants-avatars/blob.jpg"
    )
    assert participant_type.website == "https://google.it"
    assert participant_type.twitter_handle == "marco"
    assert participant_type._speaker_level == "intermediate"
    assert participant_type._previous_talk_video == ""


def test_user_participant_when_it_doesnt_exist(user, conference_factory):
    user = User.resolve_reference(user.id, user.email)
    participant_type = user.participant(info=None, conference=conference_factory().code)

    assert participant_type is None
