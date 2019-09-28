from i18n.strings import LazyI18nString
from pytest import mark


@mark.django_db
def test_get_conference_copy(conference_factory, generic_copy_factory, graphql_client):
    conference = conference_factory()
    conference_b = conference_factory()

    generic_copy_factory(
        conference=conference, key="intro", content=LazyI18nString({"en": "hello!"})
    )

    resp = graphql_client.query(
        """
        query($code: String!, $key: String!) {
            conference(code: $code) {
                copy(key: $key)
            }
        }
        """,
        variables={"code": conference.code, "key": "intro"},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["copy"] == "hello!"

    resp = graphql_client.query(
        """
        query($code: String!, $key: String!) {
            conference(code: $code) {
                copy(key: $key)
            }
        }
        """,
        variables={"code": conference_b.code, "key": "intro"},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["copy"] is None
