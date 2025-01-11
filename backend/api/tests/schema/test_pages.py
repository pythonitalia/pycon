from conferences.tests.factories import ConferenceFactory
from pytest import mark

from i18n.strings import LazyI18nString
from pages.tests.factories import PageFactory


def _query_pages(client, conference_code):
    return client.query(
        """query Pages($code: String!) {
            pages(code: $code) {
                id
                title
                slug
                content
                image
            }
        }""",
        variables={"code": conference_code},
    )


def _get_image_url(request, image):
    if not image:
        return None

    return request.build_absolute_uri(image.url)


@mark.django_db
def test_query_pages(
    rf,
    graphql_client,
):
    conference_1 = ConferenceFactory(code="pycon11")
    conference_2 = ConferenceFactory(code="pycon10")
    PageFactory(published=False, conference=conference_1)
    PageFactory(published=True, conference=conference_2)
    page = PageFactory(published=True, conference=conference_1)

    request = rf.get("/")

    resp = _query_pages(graphql_client, conference_code=conference_1.code)

    assert not resp.get("errors")

    assert len(resp["data"]["pages"]) == 1

    assert {
        "id": str(page.id),
        "title": str(page.title),
        "slug": str(page.slug),
        "content": str(page.content),
        "image": _get_image_url(request, page.image),
    } == resp["data"]["pages"][0]


@mark.django_db
def test_query_single_page(
    rf,
    graphql_client,
):
    request = rf.get("/")
    page = PageFactory(
        slug=LazyI18nString({"en": "demo"}),
        published=True,
        image=None,
        conference__code="pycon11",
    )

    resp = graphql_client.query(
        """query {
            page(code: "pycon11", slug: "demo") {
                id
                title
                slug
                content
                image
            }
        } """
    )

    assert not resp.get("errors")
    assert {
        "id": str(page.id),
        "title": str(page.title),
        "slug": str(page.slug),
        "content": str(page.content),
        "image": _get_image_url(request, page.image),
    } == resp["data"]["page"]

    resp = graphql_client.query(
        """query {
            page(slug: "demo", code: "pyconb") {
                id
            }
        } """
    )

    assert resp["data"]["page"] is None


@mark.django_db
def test_passing_language(
    graphql_client,
):
    PageFactory(
        title=LazyI18nString({"en": "this is a test", "it": "questa è una prova"}),
        slug=LazyI18nString({"en": "slug", "it": "lumaca"}),
        content=LazyI18nString({"en": "content", "it": "contenuto"}),
        published=True,
        image=None,
        conference__code="pycon11",
    )

    resp = graphql_client.query(
        """query {
            page(code: "pycon11", slug: "slug") {
                title(language: "it")
                slug(language: "it")
            }
        } """
    )

    assert not resp.get("errors")
    assert resp["data"]["page"] == {"title": "questa è una prova", "slug": "lumaca"}


@mark.django_db
@mark.skip(reason="disabled for now")
def test_defaults_on_browser_language(
    graphql_client,
):
    PageFactory(
        title=LazyI18nString({"en": "this is a test", "it": "questa è una prova"}),
        slug=LazyI18nString({"en": "slug", "it": "lumaca"}),
        content=LazyI18nString({"en": "content", "it": "contenuto"}),
        published=True,
        image=None,
        conference__code="pycon11",
    )

    headers = {"HTTP_ACCEPT_LANGUAGE": "it;q=0.8,de;q=0.7,la;q=0.6"}

    resp = graphql_client.query(
        """query {
            page(code: "pycon11", slug: "slug") {
                title
                slug
            }
        } """,
        headers=headers,
    )

    assert not resp.get("errors")
    assert resp["data"]["page"] == {"title": "questa è una prova", "slug": "lumaca"}
