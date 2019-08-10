from datetime import timedelta

from django.utils import timezone
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
def test_query_blog_posts(graphql_client, user_factory, post_factory):
    past_post = post_factory(published=timezone.now() - timedelta(days=1), image=None)
    present_post = post_factory()

    post_factory(published=timezone.now() + timedelta(days=1))

    resp = _query_blog_posts(graphql_client)

    assert len(resp["data"]["blogPosts"]) == 2

    assert {
        "id": str(past_post.id),
        "title": past_post.title,
        "slug": past_post.slug,
        "excerpt": past_post.excerpt,
        "content": past_post.content,
        "published": past_post.published.isoformat(),
        "image": str(past_post.image),
        "author": {"id": str(past_post.author.id), "email": past_post.author.email},
    } == resp["data"]["blogPosts"][1]

    assert {
        "id": str(present_post.id),
        "title": present_post.title,
        "slug": present_post.slug,
        "excerpt": present_post.excerpt,
        "content": present_post.content,
        "published": present_post.published.isoformat(),
        "image": str(present_post.image),
        "author": {
            "id": str(present_post.author.id),
            "email": present_post.author.email,
        },
    } == resp["data"]["blogPosts"][0]


@mark.django_db
def test_query_single_post(graphql_client, user_factory, post_factory):
    post = post_factory(
        slug="demo", published=timezone.now() - timedelta(days=1), image=None
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
        "title": post.title,
        "slug": post.slug,
        "excerpt": post.excerpt,
        "content": post.content,
        "published": post.published.isoformat(),
        "image": str(post.image),
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
