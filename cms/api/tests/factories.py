from page.models import GenericPage
from page.blocks import TextSection, Map, BodyBlock
from wagtail_factories import (
    CharBlockFactory,
    StreamBlockFactory,
    ImageChooserBlockFactory,
    StructBlockFactory,
    PageFactory,
    StreamFieldFactory,
)
import factory
from decimal import Decimal
from pytest_factoryboy import register
from wagtail.rich_text import RichText


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
class BodyBlockFactory(StreamBlockFactory):
    text_section = factory.SubFactory(TextSectionFactory)
    map = factory.SubFactory(MapFactory)
    image = factory.SubFactory(ImageChooserBlockFactory)

    class Meta:
        model = BodyBlock


@register
class GenericPageFactory(PageFactory):
    body = StreamFieldFactory(BodyBlockFactory)

    class Meta:
        model = GenericPage
