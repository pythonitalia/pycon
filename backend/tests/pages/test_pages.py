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
        "title": page.title,
        "slug": page.slug,
        "content": page.content,
        "image": _get_image_url(request, page.image),
    } == resp["data"]["pages"][0]


@mark.django_db
def test_query_single_page(rf, graphql_client, user_factory, page_factory):
    request = rf.get("/")
    page = page_factory(
        slug="demo", published=True, image=None, conference__code="pycon11"
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
        "title": page.title,
        "slug": page.slug,
        "content": page.content,
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
