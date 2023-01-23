import pytest


@pytest.mark.django_db
def test_returns_tags(graphql_client, submission_tag_factory):
    tag = submission_tag_factory()

    resp = graphql_client.query(
        """{
            submissionTags {
                id
            }
        }"""
    )

    assert not resp.get("errors")
    assert resp["data"]["submissionTags"] == [{"id": str(tag.id)}]


@pytest.mark.django_db
def test_returns_voting_tags(
    graphql_client, submission_tag_factory, submission_factory
):
    tag_1 = submission_tag_factory()
    submission_tag_factory()

    submission = submission_factory()
    submission.tags.add(tag_1.id)

    resp = graphql_client.query(
        """query($conference: ID!) {
            votingTags(conference: $conference) {
                id
            }
        }""",
        variables={
            "conference": submission.conference.code,
        },
    )

    assert not resp.get("errors")
    assert resp["data"]["votingTags"] == [{"id": str(tag_1.id)}]
