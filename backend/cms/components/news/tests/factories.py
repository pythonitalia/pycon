from pytest_factoryboy import register
from wagtail_factories import (
    PageFactory,
)
from cms.components.news.models import NewsArticle
from wagtail.rich_text import RichText
import factory


@register
class NewsArticleFactory(PageFactory):
    class Meta:
        model = NewsArticle

    excerpt = "Test"
    body = factory.LazyAttribute(lambda o: RichText(f"<h2>{o.h2}</h2>" f"<p>{o.p}</p>"))

    class Params:
        h2 = factory.Faker("text", max_nb_chars=20)
        p = factory.Faker("text", max_nb_chars=300)
