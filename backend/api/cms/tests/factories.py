from cms.components.page.blocks.homepage_hero import HomepageHero
from cms.components.page.models import GenericPage
from cms.components.page.blocks.text_section import TextSection
from cms.components.page.blocks.slider_cards_section import (
    SimpleTextCard,
    SliderCardsSection,
)
from cms.components.page.models import BodyBlock
from cms.components.base.blocks.map import Map
from wagtail_factories import (
    CharBlockFactory,
    StreamBlockFactory,
    StructBlockFactory,
    PageFactory,
    StreamFieldFactory,
    SiteFactory,
)
from wagtail.models import Site
import factory
from decimal import Decimal
from pytest_factoryboy import register
from wagtail.rich_text import RichText


register(PageFactory)


@register
class MapFactory(StructBlockFactory):
    latitude = Decimal(43.766200)
    longitude = Decimal(11.272250)
    zoom = 15

    class Meta:
        model = Map


@register
class TextSectionFactory(StructBlockFactory):
    title = factory.SubFactory(CharBlockFactory)
    subtitle = factory.SubFactory(CharBlockFactory)
    body = factory.LazyAttribute(lambda o: RichText(f"<h2>{o.h2}</h2>" f"<p>{o.p}</p>"))
    illustration = factory.SubFactory(CharBlockFactory)

    class Meta:
        model = TextSection

    class Params:
        h2 = factory.Faker("text", max_nb_chars=20)
        p = factory.Faker("text", max_nb_chars=300)


@register
class SimpleTextCardFactory(StructBlockFactory):
    title = factory.SubFactory(CharBlockFactory)
    body = factory.LazyAttribute(lambda o: RichText(f"<h2>{o.h2}</h2>" f"<p>{o.p}</p>"))

    class Meta:
        model = SimpleTextCard

    class Params:
        h2 = factory.Faker("text", max_nb_chars=20)
        p = factory.Faker("text", max_nb_chars=300)


@register
class HomepageHeroFactory(StructBlockFactory):
    class Meta:
        model = HomepageHero


@register
class SliderCardsSectionFactory(StreamBlockFactory):
    cards = factory.SubFactory(SimpleTextCardFactory)

    class Meta:
        model = SliderCardsSection


@register
class BodyBlockFactory(StreamBlockFactory):
    text_section = factory.SubFactory(TextSectionFactory)
    map = factory.SubFactory(MapFactory)

    class Meta:
        model = BodyBlock


@register
class GenericPageFactory(PageFactory):
    body = StreamFieldFactory(BodyBlockFactory)

    class Meta:
        model = GenericPage


@register
class SiteFactory(SiteFactory):
    """
    Overrides wagtail_factories.SiteFactory to use "testserver" as hostname
    to make sure it works with Wagtail's ALLOWED_HOSTS in test environments.
    """

    hostname = "testserver"
    root_page = factory.SubFactory(GenericPageFactory)
    is_default_site = True

    class Meta:
        model = Site
