from submissions.tests.factories import SubmissionFactory, SubmissionTagFactory
import pytest


pytestmark = pytest.mark.django_db


def test_returns_tags(graphql_client):
    tag = SubmissionTagFactory()

    resp = graphql_client.query(
        """{
            submissionTags {
                id
            }
        }"""
    )

    assert not resp.get("errors")
    assert resp["data"]["submissionTags"] == [{"id": str(tag.id)}]


def test_returns_voting_tags(graphql_client):
    tag_1 = SubmissionTagFactory()
    SubmissionTagFactory()

    submission = SubmissionFactory()
    submission.tags.add(tag_1.id)

    resp = graphql_client.query(
        """query($conference: String!) {
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
