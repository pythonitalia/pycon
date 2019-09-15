from api.voting.types import VoteValues


def test_get_enum_member_from_int():
    assert VoteValues.from_int(0) == VoteValues.NOT_INTERESTED


def test_not_found_int_returns_none():
    assert VoteValues.from_int(9999) is None
