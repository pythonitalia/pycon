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
