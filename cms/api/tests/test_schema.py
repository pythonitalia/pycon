from decimal import Decimal
import pytest

pytestmark = pytest.mark.django_db


def test_page(graphql_client, generic_page_factory, locale, image_file, site_factory):
    parent = generic_page_factory()
    page = generic_page_factory(
        slug="bubble-tea",
        locale=locale("en"),
        parent=parent,
        body__0__text_section__title__value="I've Got a Lovely Bunch of Coconuts",
        body__1__map__longitude=Decimal(3.14),
        body__2__image__image__title="Zazu",
        body__2__image__image__file=next(image_file()),
    )
    site_factory(hostname="pycon", root_page=page)
    page.copy_for_translation(locale=locale("it"))
    image = page.body[-1].value
    query = """
    query Page ($code: String!, $locale: String!, $slug: String!) {
        page(code: $code, locale: $locale, slug: $slug){
            ...on GenericPage {
                body {
                    ...on TextSection {
                        title
                    }
                    ...on Map {
                        latitude
                        longitude
                    }
                    ...on Image {
                        title
                        width
                        height
                        url
                    }
                }
            }

        }
    }
    """

    response = graphql_client.query(
        query, variables={"code": "pycon", "slug": "bubble-tea", "locale": "en"}
    )

    assert response.data == {
        "page": {
            "body": [
                {"title": "I've Got a Lovely Bunch of " "Coconuts"},
                {
                    "latitude": "43.766199999999997771737980656325817108154296875",  # noqa: E501
                    "longitude": "3.140000000000000124344978758017532527446746826171875",  # noqa: E501
                },
                {
                    "height": 480,
                    "title": "Zazu",
                    "url": image.file.url,
                    "width": 640,
                },
            ]
        }
    }


def test_page_not_found(graphql_client, site_factory):
    site_factory(hostname="not-found")
    query = """
    query Page ($code: String!, $locale: String!, $slug: String!) {
        page(code: $code, locale: $locale, slug: $slug){
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
        query, variables={"code": "not-found", "slug": "hot-tea", "locale": "en"}
    )
    assert response.data == {"page": None}


def test_site_not_found(graphql_client):
    query = """
    query Page ($code: String!, $locale: String!, $slug: String!) {
        page(code: $code, locale: $locale, slug: $slug){
            ...on SiteNotFoundError {
                message
            }
        }
    }
    """

    response = graphql_client.query(
        query, variables={"code": "not-found", "slug": "hot-tea", "locale": "en"}
    )
    assert response.data == {"page": {"message": "Site `not-found` not found"}}
