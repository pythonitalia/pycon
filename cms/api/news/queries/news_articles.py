import strawberry
from api.news.types import NewsArticle
from wagtail.models import Site
from news.models import NewsArticle as NewsArticleModel


@strawberry.field
def news_articles(hostname: str, language: str) -> list[NewsArticle]:
    site = Site.objects.filter(hostname=hostname).first()

    if not site:
        raise ValueError(f"Site {hostname} not found")

    return [
        NewsArticle.from_model(article)
        for article in NewsArticleModel.objects.in_site(site)
        .order_by("-first_published_at")
        .filter(
            locale__language_code=language,
        )
    ]
