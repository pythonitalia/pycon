from decimal import Decimal
import pytest

pytestmark = pytest.mark.django_db


def test_page(graphql_client, generic_page_factory, locale, site_factory):
    parent = generic_page_factory()
    page = generic_page_factory(
        slug="bubble-tea",
        locale=locale("en"),
        parent=parent,
        title="Bubble",
        body__0__text_section__title__value="I've Got a Lovely Bunch of Coconuts",
        body__1__map__longitude=Decimal(3.14),
    )
    site_factory(hostname="pycon", root_page=parent)
    page.copy_for_translation(locale=locale("it"))
    query = """
    query Page ($hostname: String!, $language: String!, $slug: String!) {
        cmsPage(hostname: $hostname, language: $language, slug: $slug){
            ...on GenericPage {
                title
                slug
                body {
                    ...on TextSection {
                        title
                    }
                    ...on CMSMap {
                        latitude
                        longitude
                    }
                }
            }
        }
    }
    """

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "slug": "bubble-tea", "language": "en"}
    )

    assert response.data == {
        "cmsPage": {
            "title": "Bubble",
            "slug": "bubble-tea",
            "body": [
                {"title": "I've Got a Lovely Bunch of " "Coconuts"},
                {
                    "latitude": "43.766199999999997771737980656325817108154296875",  # noqa: E501
                    "longitude": "3.140000000000000124344978758017532527446746826171875",  # noqa: E501
                },
            ],
        }
    }


def test_page_for_unknown_locale(
    graphql_client, generic_page_factory, locale, site_factory
):
    parent = generic_page_factory()
    page = generic_page_factory(
        slug="bubble-tea",
        locale=locale("en"),
        parent=parent,
        title="Bubble",
        body__0__text_section__title__value="I've Got a Lovely Bunch of Coconuts",
        body__1__map__longitude=Decimal(3.14),
    )
    site_factory(hostname="pycon", root_page=parent)
    page.copy_for_translation(locale=locale("it"))
    query = """
    query Page ($hostname: String!, $language: String!, $slug: String!) {
        cmsPage(hostname: $hostname, language: $language, slug: $slug){
            ...on GenericPage {
                title
                body {
                    ...on TextSection {
                        title
                    }
                }
            }
        }
    }
    """

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "slug": "bubble-tea", "language": "de"}
    )

    assert response.data == {"cmsPage": None}


def test_page_not_found(graphql_client, site_factory):
    site_factory(hostname="not-found")
    query = """
    query Page ($hostname: String!, $language: String!, $slug: String!) {
        cmsPage(hostname: $hostname, language: $language, slug: $slug){
            ...on GenericPage {
                body {
                    ...on TextSection {
                        title
                    }
                }
            }
        }
    }
    """

    response = graphql_client.query(
        query, variables={"hostname": "not-found", "slug": "hot-tea", "language": "en"}
    )
    assert response.data == {"cmsPage": None}


def test_page_site_not_found(graphql_client):
    query = """
    query Page ($hostname: String!, $language: String!, $slug: String!) {
        cmsPage(hostname: $hostname, language: $language, slug: $slug){
            ...on SiteNotFoundError {
                message
            }
        }
    }
    """

    response = graphql_client.query(
        query, variables={"hostname": "not-found", "slug": "hot-tea", "language": "en"}
    )
    assert response.data == {"cmsPage": {"message": "Site `not-found` not found"}}


def test_pages(graphql_client, site_factory, generic_page_factory, locale):
    parent = generic_page_factory()
    generic_page_factory(
        slug="bubble-tea",
        locale=locale("en"),
        parent=parent,
        body__0__text_section__title__value="I've Got a Lovely Bunch of Coconuts",
    )
    generic_page_factory(
        slug="chocolate",
        locale=locale("en"),
        parent=parent,
        body__0__text_section__title__value="There they are, all standing in a row",
    )
    site_factory(hostname="pycon", root_page=parent)

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

    assert response.data == {
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

    assert response.data == {"cmsPages": []}


def test_page_filter_by_site_and_language(
    graphql_client, site_factory, generic_page_factory, locale
):
    root_site_1 = generic_page_factory()
    root_site_2 = generic_page_factory()
    page_1 = generic_page_factory(
        slug="bubble-tea",
        locale=locale("en"),
        parent=root_site_1,
        body__0__text_section__title__value="I've Got a Lovely Bunch of Coconuts",
    )
    page_2 = generic_page_factory(
        slug="chocolate",
        locale=locale("en"),
        parent=root_site_2,
        body__0__text_section__title__value="There they are, all standing in a row",
    )
    site_factory(hostname="site1", root_page=root_site_1)
    site_factory(hostname="site2", root_page=root_site_2)
    page_1.copy_for_translation(locale=locale("it"))
    page_2.copy_for_translation(locale=locale("it"))

    query = """
     query Page ($hostname: String!, $language: String!, $slug: String!) {
        cmsPage(hostname: $hostname, language: $language, slug: $slug){
            ...on GenericPage {
                body {
                    ...on TextSection {
                        title
                    }
                }
            }
        }
    }
    """

    response = graphql_client.query(
        query, variables={"hostname": "site2", "slug": "chocolate", "language": "en"}
    )

    assert response.data == {
        "cmsPage": {"body": [{"title": "There they are, all standing in a row"}]}
    }
