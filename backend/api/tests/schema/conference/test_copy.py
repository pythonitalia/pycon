from cms.tests.factories import GenericCopyFactory
from conferences.tests.factories import ConferenceFactory
from pytest import mark

from i18n.strings import LazyI18nString


@mark.django_db
def test_get_conference_copy(graphql_client):
    conference = ConferenceFactory()
    conference_b = ConferenceFactory()

    GenericCopyFactory(
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
