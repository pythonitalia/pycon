import datetime
import pytest

pytestmark = pytest.mark.django_db


def test_get_news_articles(
    graphql_client,
    generic_page_factory,
    news_article_factory,
    site_factory,
    create_user,
):
    user = create_user(username="test")
    parent = generic_page_factory()
    article_1 = news_article_factory(
        title="Article 1",
        parent=parent,
        owner=user,
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    article_2 = news_article_factory(
        title="Article 2",
        parent=parent,
        owner=user,
        first_published_at=datetime.datetime(2012, 1, 1, 10, 0, 0),
    )
    site_factory(hostname="pycon", root_page=parent)

    parent_2 = generic_page_factory()
    news_article_factory(title="Invalid", parent=parent_2)
    site_factory(hostname="pycon2", root_page=parent_2)

    query = """query NewsArticles($hostname: String!, $language: String!) {
        newsArticles(hostname: $hostname, language: $language) {
            id
            title
        }
    }"""

    response = graphql_client.query(
        query, variables={"hostname": "pycon", "language": "en"}
    )

    assert response.data["newsArticles"] == [
        {"id": str(article_2.id), "title": article_2.title},
        {"id": str(article_1.id), "title": article_1.title},
    ]


def test_get_news_articles_with_invalid_site(
    graphql_client,
    generic_page_factory,
    news_article_factory,
    site_factory,
    create_user,
):
    user = create_user(username="test")
    parent = generic_page_factory()
    news_article_factory(
        title="Article 1",
        parent=parent,
        owner=user,
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    site_factory(hostname="pycon2", root_page=parent)

    query = """query NewsArticles($hostname: String!, $language: String!) {
        newsArticles(hostname: $hostname, language: $language) {
            id
            title
        }
    }"""

    response = graphql_client.query(
        query, variables={"hostname": "invalid", "language": "en"}, asserts_errors=False
    )
    assert response.errors[0]["message"] == "Site invalid not found"


def test_get_news_article(
    graphql_client,
    generic_page_factory,
    news_article_factory,
    site_factory,
    create_user,
):
    user = create_user(username="test", first_name="marco", last_name="world")
    parent = generic_page_factory()
    article_1 = news_article_factory(
        title="Article 1",
        parent=parent,
        owner=user,
        slug="slug",
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    site_factory(hostname="pycon", root_page=parent)

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

    assert response.data["newsArticle"] == {
        "id": str(article_1.id),
        "title": article_1.title,
        "authorFullname": "marco world",
    }


def test_get_news_article_another_locale(
    graphql_client,
    generic_page_factory,
    news_article_factory,
    site_factory,
    create_user,
    locale,
):
    user = create_user(username="test", first_name="marco", last_name="world")
    parent = generic_page_factory()
    article_1 = news_article_factory(
        title="Article 1",
        parent=parent,
        owner=user,
        slug="slug",
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    site_factory(hostname="pycon", root_page=parent)
    it_article = article_1.copy_for_translation(locale=locale("it"))
    it_article.title = "test"
    it_article.save()

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

    assert response.data["newsArticle"]["title"] == "test"


def test_get_news_article_with_unknown_slug(
    graphql_client,
    generic_page_factory,
    news_article_factory,
    site_factory,
    create_user,
):
    user = create_user(username="test", first_name="marco", last_name="world")
    parent = generic_page_factory()
    news_article_factory(
        title="Article 1",
        parent=parent,
        owner=user,
        slug="slug",
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    site_factory(hostname="pycon", root_page=parent)

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

    assert response.data["newsArticle"] is None


def test_get_news_article_with_unknown_locale(
    graphql_client,
    locale,
    generic_page_factory,
    news_article_factory,
    site_factory,
    create_user,
):
    user = create_user(username="test", first_name="marco", last_name="world")
    parent = generic_page_factory()
    news_article_factory(
        title="Article 1",
        parent=parent,
        locale=locale("en"),
        owner=user,
        slug="slug",
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    site_factory(hostname="pycon", root_page=parent)

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

    assert response.data["newsArticle"] is None


def test_get_news_article_with_invalid_site(
    graphql_client,
    locale,
    generic_page_factory,
    news_article_factory,
    site_factory,
    create_user,
):
    user = create_user(username="test", first_name="marco", last_name="world")
    parent = generic_page_factory()
    news_article_factory(
        title="Article 1",
        parent=parent,
        locale=locale("en"),
        owner=user,
        slug="slug",
        first_published_at=datetime.datetime(2010, 1, 1, 10, 0, 0),
    )
    site_factory(hostname="pycon", root_page=parent)

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
        asserts_errors=False,
    )

    assert response.errors[0]["message"] == "Site invalid not found"
