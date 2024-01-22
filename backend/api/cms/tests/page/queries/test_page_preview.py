from cms.components.news.models import NewsArticle
from cms.components.news.tests.factories import NewsArticleFactory
from cms.components.page.models import GenericPage
from django.contrib.contenttypes.models import ContentType

import pytest
from api.cms.tests.factories import GenericPageFactory, SiteFactory

pytestmark = pytest.mark.django_db


def test_page_preview_for_pages(graphql_client, locale):
    parent = GenericPageFactory()
    parent.save_revision().publish()
    page_1 = GenericPageFactory(
        title="Bubble Tea",
        slug="bubble-tea",
        locale=locale("en"),
        parent=parent,
        body__0__text_section__title__value="I've Got a Lovely Bunch of Coconuts",
    )
    SiteFactory(hostname="pycon", port=80, root_page=parent)
    page_preview = page_1.create_page_preview()

    query = """
    query Preview ($contentType: String!, $token: String!) {
        pagePreview(contentType: $contentType, token: $token){
            __typename
            ... on GenericPagePreview {
                genericPage {
                    title
                }
            }
        }
    }
    """

    content_type = ".".join(
        ContentType.objects.get_for_model(GenericPage).natural_key()
    )
    response = graphql_client.query(
        query, variables={"contentType": content_type, "token": page_preview.token}
    )

    assert response["data"] == {
        "pagePreview": {
            "__typename": "GenericPagePreview",
            "genericPage": {
                "title": "Bubble Tea",
            },
        }
    }


def test_page_preview_for_news_article(graphql_client, locale):
    parent = GenericPageFactory()
    parent.save_revision().publish()
    news_article = NewsArticleFactory(
        title="Bubble Tea",
        slug="bubble-tea",
        locale=locale("en"),
        parent=parent,
    )
    SiteFactory(hostname="pycon", port=80, root_page=parent)
    page_preview = news_article.create_page_preview()

    query = """
    query Preview ($contentType: String!, $token: String!) {
        pagePreview(contentType: $contentType, token: $token){
            __typename
            ... on NewsArticlePreview {
                newsArticle {
                    title
                }
            }
        }
    }
    """

    content_type = ".".join(
        ContentType.objects.get_for_model(NewsArticle).natural_key()
    )
    response = graphql_client.query(
        query, variables={"contentType": content_type, "token": page_preview.token}
    )

    assert response["data"] == {
        "pagePreview": {
            "__typename": "NewsArticlePreview",
            "newsArticle": {
                "title": "Bubble Tea",
            },
        }
    }


def test_page_preview_with_invalid_token(graphql_client, locale):
    parent = GenericPageFactory()
    parent.save_revision().publish()
    page_1 = GenericPageFactory(
        title="Bubble Tea",
        slug="bubble-tea",
        locale=locale("en"),
        parent=parent,
        body__0__text_section__title__value="I've Got a Lovely Bunch of Coconuts",
    )
    SiteFactory(hostname="pycon", port=80, root_page=parent)
    page_1.create_page_preview()

    query = """
    query Preview ($contentType: String!, $token: String!) {
        pagePreview(contentType: $contentType, token: $token){
            __typename
            ... on GenericPagePreview {
                genericPage {
                    title
                }
            }
        }
    }
    """

    content_type = ".".join(
        ContentType.objects.get_for_model(GenericPage).natural_key()
    )
    response = graphql_client.query(
        query, variables={"contentType": content_type, "token": "random-token"}
    )

    assert response["data"] == {"pagePreview": None}


def test_page_preview_with_invalid_content_type(graphql_client, locale):
    parent = GenericPageFactory()
    parent.save_revision().publish()
    page_1 = GenericPageFactory(
        title="Bubble Tea",
        slug="bubble-tea",
        locale=locale("en"),
        parent=parent,
        body__0__text_section__title__value="I've Got a Lovely Bunch of Coconuts",
    )
    SiteFactory(hostname="pycon", port=80, root_page=parent)
    page_review = page_1.create_page_preview()

    query = """
    query Preview ($contentType: String!, $token: String!) {
        pagePreview(contentType: $contentType, token: $token){
            __typename
            ... on GenericPagePreview {
                genericPage {
                    title
                }
            }
        }
    }
    """

    response = graphql_client.query(
        query, variables={"contentType": "not.content_type", "token": page_review.token}
    )

    assert response["data"] == {"pagePreview": None}
