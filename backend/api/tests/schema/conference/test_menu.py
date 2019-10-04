from pytest import mark


@mark.django_db
def test_get_menu_not_found(graphql_client, conference_factory):
    conference = conference_factory()

    resp = graphql_client.query(
        """
        query($code: String!, $identifier: String!) {
            conference(code: $code) {
                menu(identifier: $identifier) {
                    links {
                        title
                        href
                        target
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
def test_get_menu(graphql_client, conference_factory, menu_factory, menu_link_factory):
    conference = conference_factory()

    menu = menu_factory(identifier="main-nav", conference=conference)

    menu_link_factory.create_batch(3, menu=menu)

    resp = graphql_client.query(
        """
        query($code: String!, $identifier: String!) {
            conference(code: $code) {
                menu(identifier: $identifier) {
                    links {
                        title
                        href
                        target
                    }
                }
            }
        }
        """,
        variables={"code": conference.code, "identifier": "main-nav"},
    )

    assert "errors" not in resp
    assert len(resp["data"]["conference"]["menu"]["links"]) == 3
