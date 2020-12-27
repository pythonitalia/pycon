from datetime import timedelta

from django.utils import timezone
from helpers.tests import get_image_url_from_request
from i18n.strings import LazyI18nString
from pytest import mark


def _query_blog_posts(client):
    return client.query(
        """
        query {
            blogPosts {
                id
                title
                slug
                excerpt
                content
                published
                image
                author {
                    id
                    email
                }
            }
        }
    """
    )


@mark.django_db
def test_query_blog_posts(rf, graphql_client, user_factory, post_factory):
    past_post = post_factory(published=timezone.now() - timedelta(days=1), image=None)
    present_post = post_factory()

    request = rf.get("/")

    post_factory(published=timezone.now() + timedelta(days=1))

    resp = _query_blog_posts(graphql_client)

    assert len(resp["data"]["blogPosts"]) == 2

    assert {
        "id": str(past_post.id),
        "title": str(past_post.title),
        "slug": str(past_post.slug),
        "excerpt": str(past_post.excerpt),
        "content": str(past_post.content),
        "published": past_post.published.isoformat(),
        "image": get_image_url_from_request(request, past_post.image),
        "author": {"id": str(past_post.author.id), "email": past_post.author.email},
    } == resp["data"]["blogPosts"][1]

    assert {
        "id": str(present_post.id),
        "title": str(present_post.title),
        "slug": str(present_post.slug),
        "excerpt": str(present_post.excerpt),
        "content": str(present_post.content),
        "published": present_post.published.isoformat(),
        "image": get_image_url_from_request(request, present_post.image),
        "author": {
            "id": str(present_post.author.id),
            "email": present_post.author.email,
        },
    } == resp["data"]["blogPosts"][0]


@mark.django_db
def test_query_single_post(rf, graphql_client, user_factory, post_factory):
    request = rf.get("/")
    post = post_factory(
        slug=LazyI18nString({"en": "demo", "it": "esempio"}),
        published=timezone.now() - timedelta(days=1),
        image=None,
    )

    resp = graphql_client.query(
        """query {
            blogPost(slug: "demo") {
                id
                title
                slug
                excerpt
                content
                published
                image
                author {
                    id
                    email
                }
            }
        } """
    )

    assert {
        "id": str(post.id),
        "title": str(post.title),
        "slug": str(post.slug),
        "excerpt": str(post.excerpt),
        "content": str(post.content),
        "published": post.published.isoformat(),
        "image": get_image_url_from_request(request, post.image),
        "author": {"id": str(post.author.id), "email": post.author.email},
    } == resp["data"]["blogPost"]

    resp = graphql_client.query(
        """query {
            blogPost(slug: "donut") {
                id
            }
        } """
    )

    assert resp["data"]["blogPost"] is None


@mark.django_db
def test_passing_language(graphql_client, post_factory):
    post_factory(
        title=LazyI18nString({"en": "this is a test", "it": "questa è una prova"}),
        slug=LazyI18nString({"en": "slug", "it": "lumaca"}),
        content=LazyI18nString({"en": "content", "it": "contenuto"}),
        excerpt=LazyI18nString({"en": "excerpt", "it": "sommario"}),
        published=timezone.now() - timedelta(days=1),
        image=None,
    )

    resp = graphql_client.query(
        """query {
            blogPost(slug: "slug") {
                title(language: "it")
                slug(language: "it")
                content(language: "it")
                excerpt(language: "it")
            }
        } """
    )

    assert not resp.get("errors")
    assert resp["data"]["blogPost"] == {
        "title": "questa è una prova",
        "slug": "lumaca",
        "content": "contenuto",
        "excerpt": "sommario",
    }
