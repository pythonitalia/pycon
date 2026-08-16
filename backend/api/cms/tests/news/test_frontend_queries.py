import datetime

import pytest
from wagtail.rich_text import RichText

from api.cms.tests.factories import GenericPageFactory, SiteFactory
from cms.components.news.tests.factories import NewsArticleFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


ALL_NEWS_ARTICLES_QUERY = """\
query AllNewsArticles($hostname: String!) {
  newsArticles(hostname: $hostname, language: "en") {
    id
    slug
  }
}
"""


NEWS_ARTICLE_QUERY = """\
query NewsArticle($hostname: String!, $slug: String!) {
  newsArticle(hostname: $hostname, slug: $slug, language: "en") {
    id
    title
    excerpt
    body
    publishedAt
    authorFullname
  }
}
"""


def test_all_news_articles_frontend_query(
    graphql_client,
    django_assert_num_queries,
):
    parent = GenericPageFactory()
    articles = []

    for index in range(4):
        article = NewsArticleFactory(
            title=f"Article {index}",
            slug=f"article-{index}",
            parent=parent,
            owner=UserFactory(full_name=f"Author {index}"),
            first_published_at=datetime.datetime(
                2026,
                1,
                index + 1,
                10,
                0,
                tzinfo=datetime.UTC,
            ),
        )
        article.save_revision().publish()
        articles.append(article)

    SiteFactory(hostname="pycon", port=80, root_page=parent)

    with django_assert_num_queries(3):
        response = graphql_client.query(
            ALL_NEWS_ARTICLES_QUERY,
            variables={"hostname": "pycon"},
        )

    assert response == {
        "data": {
            "newsArticles": [
                {"id": str(article.id), "slug": article.slug}
                for article in reversed(articles)
            ]
        }
    }


def test_news_article_frontend_query(
    graphql_client,
    django_assert_num_queries,
):
    published_at = datetime.datetime(2026, 1, 1, 10, 0, tzinfo=datetime.UTC)
    parent = GenericPageFactory()
    article = NewsArticleFactory(
        title="Strawberry Fields",
        slug="strawberry-fields",
        excerpt="A GraphQL story",
        body=RichText("<p>News article body</p>"),
        parent=parent,
        owner=UserFactory(full_name="Ada Strawberry"),
        first_published_at=published_at,
    )
    article.save_revision().publish()
    SiteFactory(hostname="pycon", port=80, root_page=parent)

    with django_assert_num_queries(4):
        response = graphql_client.query(
            NEWS_ARTICLE_QUERY,
            variables={
                "hostname": "pycon",
                "slug": article.slug,
            },
        )

    assert response == {
        "data": {
            "newsArticle": {
                "id": str(article.id),
                "title": "Strawberry Fields",
                "excerpt": "A GraphQL story",
                "body": "<p>News article body</p>",
                "publishedAt": published_at.isoformat(),
                "authorFullname": "Ada Strawberry",
            }
        }
    }
