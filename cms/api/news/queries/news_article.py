import strawberry
from api.news.types import NewsArticle
from wagtail.models import Site
from news.models import NewsArticle as NewsArticleModel


@strawberry.field
def news_article(hostname: str, slug: str, language: str) -> NewsArticle | None:
    site = Site.objects.filter(hostname=hostname).first()

    if not site:
        raise ValueError(f"Site {hostname} not found")

    article = (
        NewsArticleModel.objects.in_site(site)
        .filter(
            locale__language_code=language,
        )
        .filter(slug=slug)
        .first()
    )

    if not article:
        return None

    translated_article = (
        article.get_translations(inclusive=True)
        .filter(locale__language_code=language)
        .first()
    )

    if not translated_article:
        return None

    return NewsArticle.from_model(translated_article)
