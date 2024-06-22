from files_upload.tests.factories import FileFactory
from submissions.tests.factories import ProposalMaterialFactory
from pytest import mark

from api.helpers.ids import encode_hashid
from schedule.models import ScheduleItem
from schedule.tests.factories import ScheduleItemFactory

pytestmark = mark.django_db


def test_returns_none_when_missing(graphql_client):
    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
            }
        }""",
        variables={"id": encode_hashid(11)},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"] is None


def test_returns_none_with_invalid_id_string(graphql_client):
    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
            }
        }""",
        variables={"id": "invalid"},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"] is None


def test_returns_correct_submission(graphql_client, user, submission_factory):
    graphql_client.force_login(user)
    submission = submission_factory(speaker_id=user.id)

    resp = graphql_client.query(
        """query SubmissionQuery($id: ID!) {
            submission(id: $id) {
                id
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert not resp.get("errors")
    assert resp["data"]["submission"]["id"] == submission.hashid


def test_user_can_edit_submission_if_within_cfp_time_and_is_the_owner(
    graphql_client, user, submission_factory
):
    graphql_client.force_login(user)
    submission = submission_factory(speaker_id=user.id, conference__active_cfp=True)

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                canEdit
            }
        }
    """,
        variables={"id": submission.hashid},
    )

    assert response["data"]["submission"]["canEdit"] is True


def test_cannot_edit_submission_if_not_the_owner(
    graphql_client, user, submission_factory
):
    graphql_client.force_login(user)
    submission = submission_factory(conference__active_cfp=True)
    ScheduleItemFactory(
        conference=submission.conference,
        submission=submission,
        type=ScheduleItem.TYPES.talk,
    )

    response = graphql_client.query(
        """query Submission($id: ID!) {
            submission(id: $id) {
                id
                canEdit
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert response["data"]["submission"] == {"id": submission.hashid, "canEdit": False}


def test_can_edit_submission_if_cfp_is_closed(graphql_client, user, submission_factory):
    graphql_client.force_login(user)
    submission = submission_factory(speaker_id=user.id, conference__active_cfp=False)

    response = graphql_client.query(
        """
        query Submission($id: ID!) {
            submission(id: $id) {
                id
                canEdit
            }
        }
    """,
        variables={"id": submission.hashid},
    )

    assert response["data"]["submission"]["canEdit"] is True


def test_cannot_see_submissions_if_restricted(graphql_client, user, submission_factory):
    graphql_client.force_login(user)
    submission = submission_factory(conference__active_cfp=True)

    response = graphql_client.query(
        """query Submission($id: ID!) {
            submission(id: $id) {
                id
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert response["data"]["submission"] is None


def test_can_see_submissions_while_voting_with_ticket(
    graphql_client, user, submission_factory, mock_has_ticket
):
    graphql_client.force_login(user)
    submission = submission_factory(
        conference__active_cfp=False, conference__active_voting=True
    )
    mock_has_ticket(submission.conference)

    response = graphql_client.query(
        """query Submission($id: ID!) {
            submission(id: $id) {
                id
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert response["data"]["submission"]["id"] == submission.hashid


def test_submission_materials(
    graphql_client, user, submission_factory, mock_has_ticket
):
    graphql_client.force_login(user)
    submission = submission_factory(
        conference__active_cfp=False, conference__active_voting=True
    )
    material_1 = ProposalMaterialFactory(
        proposal=submission, name="test", url="https://example.com"
    )
    material_2 = ProposalMaterialFactory(
        proposal=submission,
        name="material 2",
        file=FileFactory(
            mime_type="application/pdf",
        ),
    )
    mock_has_ticket(submission.conference)

    response = graphql_client.query(
        """query Submission($id: ID!) {
            submission(id: $id) {
                id
                materials {
                    id
                    name
                    url
                    fileUrl
                    fileMimeType
                }
            }
        }""",
        variables={"id": submission.hashid},
    )

    assert response["data"]["submission"]["id"] == submission.hashid
    materials = response["data"]["submission"]["materials"]
    assert {
        "id": str(material_1.id),
        "name": material_1.name,
        "url": material_1.url,
        "fileUrl": None,
        "fileMimeType": None,
    } == materials[0]
    assert {
        "id": str(material_2.id),
        "name": material_2.name,
        "url": None,
        "fileUrl": material_2.file.url,
        "fileMimeType": material_2.file.mime_type,
    } == materials[1]
