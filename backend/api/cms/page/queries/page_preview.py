from typing import Union
from api.cms.news.types import NewsArticle
from api.cms.page.types import GenericPage
import strawberry
from django.contrib.contenttypes.models import ContentType
from wagtail_headless_preview.models import PagePreview
from cms.components.page.models import GenericPage as GenericPageModel
from cms.components.news.models import NewsArticle as NewsArticleModel


@strawberry.type
class GenericPagePreview:
    generic_page: GenericPage


@strawberry.type
class NewsArticlePreview:
    news_article: NewsArticle


@strawberry.field
def page_preview(
    content_type: str, token: str
) -> Union[GenericPagePreview, NewsArticlePreview]:
    app_label, model = content_type.split(".")

    content_type = ContentType.objects.get(app_label=app_label, model=model)
    page_preview = PagePreview.objects.get(content_type=content_type, token=token)
    page = page_preview.as_page()

    if not page.id:
        page.id = 0

    match page:
        case GenericPageModel():
            return GenericPagePreview(generic_page=GenericPage.from_model(page))
        case NewsArticleModel():
            return NewsArticlePreview(news_article=NewsArticle.from_model(page))
        case _:
            raise ValueError(f"Unknown content type {content_type}")
