import strawberry

from api.cms.news.types import NewsArticle
from api.cms.utils import get_site_by_host
from cms.components.news import models


@strawberry.field
def news_article(hostname: str, slug: str, language: str) -> NewsArticle | None:
    site = get_site_by_host(hostname)

    if not site:
        raise ValueError(f"Site {hostname} not found")

    article = (
        models.NewsArticle.objects.in_site(site).filter(slug=slug, live=True).first()
    )

    if not article:
        return None

    translated_article = (
        article.get_translations(inclusive=True)
        .filter(locale__language_code=language, live=True)
        .first()
    )

    if not translated_article:
        return None

    return translated_article
