import strawberry
from api.cms.news.types import NewsArticle
from wagtail.models import Site
from cms.components.news.models import NewsArticle as NewsArticleModel


@strawberry.field
def news_article(hostname: str, slug: str, language: str) -> NewsArticle | None:
    hostname, port = hostname.split(":") if ":" in hostname else (hostname, 80)
    site = Site.objects.filter(hostname=hostname, port=port).first()

    if not site:
        raise ValueError(f"Site {hostname} not found")

    article = NewsArticleModel.objects.in_site(site).filter(slug=slug).first()

    if not article:
        return None

    translated_article = (
        article.get_translations(inclusive=True)
        .filter(locale__language_code=language, live=True)
        .first()
    )

    if not translated_article:
        return None

    return NewsArticle.from_model(translated_article)
