import pytest
from api.cms.tests.factories import GenericPageFactory, SiteFactory

pytestmark = pytest.mark.django_db


def test_pages(graphql_client, locale):
    parent = GenericPageFactory()
    parent.save_revision().publish()
    page_1 = GenericPageFactory(
        slug="bubble-tea",
        locale=locale("en"),
        parent=parent,
        body__0__text_section__title__value="I've Got a Lovely Bunch of Coconuts",
    )
    page_1.save_revision().publish()
    page_2 = GenericPageFactory(
        slug="chocolate",
        locale=locale("en"),
        parent=parent,
        body__0__text_section__title__value="There they are, all standing in a row",
    )
    page_2.save_revision().publish()
    SiteFactory(hostname="pycon", port=80, root_page=parent)

    query = """
    query Page ($hostname: String!, $language: String!) {
        cmsPages(hostname: $hostname, language: $language){
            body {
                ...on TextSection {
                    title
                }
            }
        }
    }
    """

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "language": "en"}
    )

    assert response["data"] == {
        "cmsPages": [
            {"body": []},
            {"body": [{"title": "I've Got a Lovely Bunch of Coconuts"}]},
            {"body": [{"title": "There they are, all standing in a row"}]},
        ]
    }


def test_pages_site_not_found(graphql_client):
    query = """
    query Page ($hostname: String!, $language: String!) {
        cmsPages(hostname: $hostname, language: $language){
            body {
                ...on TextSection {
                    title
                }
            }
        }
    }
    """

    response = graphql_client.query(
        query, variables={"hostname": "not-found", "slug": "hot-tea", "language": "en"}
    )

    assert response["data"] == {"cmsPages": []}
