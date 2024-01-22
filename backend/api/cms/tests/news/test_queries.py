import datetime
import pytest
from api.cms.tests.factories import GenericPageFactory, SiteFactory
from cms.components.news.tests.factories import NewsArticleFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_get_news_articles(
    graphql_client,
):
    user = UserFactory()
    parent = GenericPageFactory()
    article_1 = NewsArticleFactory(
        title="Article 1",
        parent=parent,
        owner=user,
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    article_1.save_revision().publish()
    article_2 = NewsArticleFactory(
        title="Article 2",
        parent=parent,
        owner=user,
        first_published_at=datetime.datetime(2012, 1, 1, 10, 0, 0),
    )
    article_2.save_revision().publish()
    NewsArticleFactory(
        title="Draft Article",
        parent=parent,
        owner=user,
        first_published_at=None,
        live=False,
    )
    SiteFactory(hostname="pycon", port=80, root_page=parent)

    parent_2 = GenericPageFactory()
    NewsArticleFactory(title="Invalid", parent=parent_2)
    SiteFactory(hostname="pycon2", root_page=parent_2)

    query = """query NewsArticles($hostname: String!, $language: String!) {
        newsArticles(hostname: $hostname, language: $language) {
            id
            title
        }
    }"""

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "language": "en"}
    )

    assert response["data"]["newsArticles"] == [
        {"id": str(article_2.id), "title": article_2.title},
        {"id": str(article_1.id), "title": article_1.title},
    ]


def test_get_news_articles_with_invalid_site(
    graphql_client,
):
    user = UserFactory()
    parent = GenericPageFactory()
    article = NewsArticleFactory(
        title="Article 1",
        parent=parent,
        owner=user,
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    article.save_revision().publish()
    SiteFactory(hostname="pycon2", root_page=parent)

    query = """query NewsArticles($hostname: String!, $language: String!) {
        newsArticles(hostname: $hostname, language: $language) {
            id
            title
        }
    }"""

    response = graphql_client.query(
        query, variables={"hostname": "invalid", "language": "en"}
    )
    assert response["errors"][0]["message"] == "Site invalid not found"


def test_get_news_article(
    graphql_client,
):
    user = UserFactory(full_name="marco world")
    parent = GenericPageFactory()
    article_1 = NewsArticleFactory(
        title="Article 1",
        parent=parent,
        owner=user,
        slug="slug",
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    article_1.save_revision().publish()
    SiteFactory(hostname="pycon", port=80, root_page=parent)

    query = """query NewsArticle(
        $hostname: String!,
        $slug: String!,
        $language: String!
    ) {
        newsArticle(hostname: $hostname, slug: $slug, language: $language) {
            id
            title
            authorFullname
        }
    }"""

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "slug": article_1.slug, "language": "en"}
    )

    assert response["data"]["newsArticle"] == {
        "id": str(article_1.id),
        "title": article_1.title,
        "authorFullname": "marco world",
    }


def test_get_news_article_returns_live_revision(
    graphql_client,
):
    user = UserFactory(full_name="marco world")
    parent = GenericPageFactory()
    article_1 = NewsArticleFactory(
        title="Article 1",
        parent=parent,
        owner=user,
        slug="slug",
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    revision_1 = article_1.save_revision()
    revision_1.publish()

    article_1.title = "Better title"
    revision_2 = article_1.save_revision(previous_revision=revision_1)

    SiteFactory(hostname="pycon", port=80, root_page=parent)

    query = """query NewsArticle(
        $hostname: String!,
        $slug: String!,
        $language: String!
    ) {
        newsArticle(hostname: $hostname, slug: $slug, language: $language) {
            id
            title
            authorFullname
        }
    }"""

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "slug": article_1.slug, "language": "en"}
    )

    assert response["data"]["newsArticle"]["title"] == "Article 1"

    revision_2.publish()

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "slug": article_1.slug, "language": "en"}
    )

    assert response["data"]["newsArticle"]["title"] == "Better title"


def test_cannot_get_draft_news_article(
    graphql_client,
):
    user = UserFactory(full_name="marco world")
    parent = GenericPageFactory()
    article_1 = NewsArticleFactory(
        title="Article 1",
        parent=parent,
        owner=user,
        slug="slug",
        first_published_at=None,
        live=False,
    )
    SiteFactory(hostname="pycon", port=80, root_page=parent)

    query = """query NewsArticle(
        $hostname: String!,
        $slug: String!,
        $language: String!
    ) {
        newsArticle(hostname: $hostname, slug: $slug, language: $language) {
            id
            title
            authorFullname
        }
    }"""

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "slug": article_1.slug, "language": "en"}
    )

    assert response["data"]["newsArticle"] is None


def test_get_news_article_another_locale(
    graphql_client,
    locale,
):
    user = UserFactory()
    parent = GenericPageFactory()
    article_1 = NewsArticleFactory(
        title="Article 1",
        parent=parent,
        owner=user,
        slug="slug",
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    article_1.save_revision().publish()
    SiteFactory(hostname="pycon", port=80, root_page=parent)
    it_article = article_1.copy_for_translation(locale=locale("it"))
    it_article.title = "test"
    it_article.save()
    it_article.save_revision().publish()

    query = """query NewsArticle(
        $hostname: String!,
        $slug: String!,
        $language: String!
    ) {
        newsArticle(hostname: $hostname, slug: $slug, language: $language) {
            id
            title
            authorFullname
        }
    }"""

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "slug": article_1.slug, "language": "it"}
    )

    assert response["data"]["newsArticle"]["title"] == "test"


def test_get_news_article_with_unknown_slug(
    graphql_client,
):
    user = UserFactory()
    parent = GenericPageFactory()
    article = NewsArticleFactory(
        title="Article 1",
        parent=parent,
        owner=user,
        slug="slug",
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    article.save_revision().publish()
    SiteFactory(hostname="pycon", port=80, root_page=parent)

    query = """query NewsArticle(
        $hostname: String!,
        $slug: String!,
        $language: String!
    ) {
        newsArticle(hostname: $hostname, slug: $slug, language: $language) {
            id
            title
            authorFullname
        }
    }"""

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "slug": "other", "language": "en"}
    )

    assert response["data"]["newsArticle"] is None


def test_get_news_article_with_unknown_locale(
    graphql_client,
    locale,
):
    user = UserFactory()
    parent = GenericPageFactory()
    article = NewsArticleFactory(
        title="Article 1",
        parent=parent,
        locale=locale("en"),
        owner=user,
        slug="slug",
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    article.save_revision().publish()
    SiteFactory(hostname="pycon", port=80, root_page=parent)

    query = """query NewsArticle(
        $hostname: String!,
        $slug: String!,
        $language: String!
    ) {
        newsArticle(hostname: $hostname, slug: $slug, language: $language) {
            id
            title
            authorFullname
        }
    }"""

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "slug": "other", "language": "de"}
    )

    assert response["data"]["newsArticle"] is None


def test_get_news_article_with_invalid_site(
    graphql_client,
    locale,
):
    user = UserFactory()
    parent = GenericPageFactory()
    article = NewsArticleFactory(
        title="Article 1",
        parent=parent,
        locale=locale("en"),
        owner=user,
        slug="slug",
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    article.save_revision().publish()
    SiteFactory(hostname="pycon", port=80, root_page=parent)

    query = """query NewsArticle(
        $hostname: String!,
        $slug: String!,
        $language: String!
    ) {
        newsArticle(hostname: $hostname, slug: $slug, language: $language) {
            id
            title
            authorFullname
        }
    }"""

    response = graphql_client.query(
        query,
        variables={"hostname": "invalid", "slug": "other", "language": "de"},
    )

    assert response["errors"][0]["message"] == "Site invalid not found"
