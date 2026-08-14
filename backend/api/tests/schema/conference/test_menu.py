from pytest import mark

from cms.tests.factories import MenuFactory, MenuLinkFactory
from conferences.tests.factories import ConferenceFactory
from pages.tests.factories import PageFactory


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


@mark.parametrize("link_count", [1, 4])
@mark.django_db
def test_frontend_header_menus_query_is_constant(
    graphql_client, django_assert_num_queries, link_count
):
    conference = ConferenceFactory()
    for identifier in ["conference-nav", "program-nav"]:
        menu = MenuFactory(identifier=identifier, conference=conference)
        for _ in range(link_count):
            MenuLinkFactory(
                menu=menu,
                page=PageFactory(conference=conference),
            )

    with django_assert_num_queries(9):
        resp = graphql_client.query(
            """
            query Header($code: String!) {
                conference(code: $code) {
                    id
                    conferenceMenuEn: menu(identifier: "conference-nav") {
                        links {
                            text: title(language: "en")
                            link: href(language: "en")
                            page {
                                slug(language: "en")
                            }
                        }
                    }
                    programMenuEn: menu(identifier: "program-nav") {
                        links {
                            text: title(language: "en")
                            link: href(language: "en")
                            page {
                                slug(language: "en")
                            }
                        }
                    }
                    conferenceMenuIt: menu(identifier: "conference-nav") {
                        links {
                            text: title(language: "it")
                            link: href(language: "it")
                            page {
                                slug(language: "it")
                            }
                        }
                    }
                    programMenuIt: menu(identifier: "program-nav") {
                        links {
                            text: title(language: "it")
                            link: href(language: "it")
                            page {
                                slug(language: "it")
                            }
                        }
                    }
                }
            }
            """,
            variables={"code": conference.code},
        )

    assert "errors" not in resp
