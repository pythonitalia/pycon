import strawberry_django

from cms.api.news.types import NewsArticle
from cms.api.utils import get_site_by_host
from cms.components.news import models


@strawberry_django.field
def news_article(hostname: str, slug: str, language: str) -> NewsArticle | None:
    site = get_site_by_host(hostname)

    if not site:
        raise ValueError(f"Site {hostname} not found")

    article = (
        models.NewsArticle.objects.in_site(site).filter(slug=slug, live=True).first()
    )

    if not article:
        return None

    return article.get_translations(inclusive=True).filter(
        locale__language_code=language, live=True
    )
