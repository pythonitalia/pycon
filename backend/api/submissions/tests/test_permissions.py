from api.submissions.permissions import IsSubmissionSpeakerOrStaff


def test_doesnt_implement_generic_permission(rf):
    assert IsSubmissionSpeakerOrStaff().has_permission(None, None) is False
