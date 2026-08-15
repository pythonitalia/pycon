import strawberry_django

from cms.api.news.types import NewsArticle
from cms.api.utils import get_site_by_host
from cms.components.news import models


@strawberry_django.field
def news_articles(hostname: str, language: str) -> list[NewsArticle]:
    site = get_site_by_host(hostname)

    if not site:
        raise ValueError(f"Site {hostname} not found")

    return (
        models.NewsArticle.objects.in_site(site)
        .order_by("-first_published_at")
        .filter(
            locale__language_code=language,
            live=True,
        )
    )
