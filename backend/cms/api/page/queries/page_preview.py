import strawberry
from django.contrib.contenttypes.models import ContentType
from wagtail_headless_preview.models import PagePreview

from cms.api.news.types import NewsArticle
from cms.api.page.types import GenericPage
from cms.components.news import models as news_models
from cms.components.page import models as page_models


@strawberry.type
class GenericPagePreview:
    generic_page: GenericPage


@strawberry.type
class NewsArticlePreview:
    news_article: NewsArticle


@strawberry.field
def page_preview(
    content_type: str, token: str
) -> GenericPagePreview | NewsArticlePreview | None:
    app_label, model = content_type.split(".")
    content_type = ContentType.objects.filter(app_label=app_label, model=model).first()

    if not content_type:
        return None

    page_preview = PagePreview.objects.filter(
        content_type=content_type, token=token
    ).first()

    if not page_preview:
        return None

    page = page_preview.as_page()

    if not page.id:
        page.id = 0

    match page:
        case page_models.GenericPage():
            return GenericPagePreview(generic_page=GenericPage.from_model(page))
        case news_models.NewsArticle():
            return NewsArticlePreview(news_article=page)
