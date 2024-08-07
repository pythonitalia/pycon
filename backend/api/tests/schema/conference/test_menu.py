from cms.tests.factories import MenuFactory, MenuLinkFactory
from conferences.tests.factories import ConferenceFactory
from pytest import mark


@mark.django_db
def test_get_menu_not_found(graphql_client):
    conference = ConferenceFactory()

    resp = graphql_client.query(
        """
        query($code: String!, $identifier: String!) {
            conference(code: $code) {
                menu(identifier: $identifier) {
                    links {
                        title
                        href
                    }
                }
            }
        }
        """,
        variables={"code": conference.code, "identifier": "main-nav"},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["menu"] is None


@mark.django_db
def test_get_menu(
    graphql_client,
):
    conference = ConferenceFactory()

    menu = MenuFactory(identifier="main-nav", conference=conference)

    MenuLinkFactory.create_batch(3, menu=menu)

    resp = graphql_client.query(
        """
        query($code: String!, $identifier: String!) {
            conference(code: $code) {
                menu(identifier: $identifier) {
                    links {
                        title
                        href
                    }
                }
            }
        }
        """,
        variables={"code": conference.code, "identifier": "main-nav"},
    )

    assert "errors" not in resp
    assert len(resp["data"]["conference"]["menu"]["links"]) == 3
