from i18n.strings import LazyI18nString
from pytest import mark


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
def test_query_pages(rf, graphql_client, user_factory, page_factory):
    page_factory(published=False, conference__code="pycon11")
    page_factory(published=True, conference__code="pycon10")
    page = page_factory(published=True, conference__code="pycon11")

    request = rf.get("/")

    resp = _query_pages(graphql_client, conference_code="pycon11")

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
def test_query_single_page(rf, graphql_client, user_factory, page_factory):
    request = rf.get("/")
    page = page_factory(
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
def test_passing_language(graphql_client, page_factory):
    page_factory(
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
def test_defaults_on_browser_language(graphql_client, page_factory):
    page_factory(
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
