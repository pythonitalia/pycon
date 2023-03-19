from wagtail import blocks

from wagtail.images.blocks import ImageChooserBlock


class CTA(blocks.StructBlock):
    label = blocks.CharBlock(required=False)
    link = blocks.CharBlock(required=False)

    class Meta:
        label = "Call to Action"
        icon = "site"


class SimpleTextCard(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock()
    cta = CTA()

    class Meta:
        label = "Card: Simple Text"
        icon = "doc-full"


class SliderCardsSection(blocks.StructBlock):
    cards = blocks.ListBlock(SimpleTextCard)

    class Meta:
        label = "Slider Cards Section"
        icon = "crosshairs"


class Accordion(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock()
    is_open = blocks.BooleanBlock(required=False, default=True)

    class Meta:
        icon = "arrow-down"


class Map(blocks.StructBlock):
    longitude = blocks.DecimalBlock(max_digits=9, decimal_places=6)
    latitude = blocks.DecimalBlock(max_digits=9, decimal_places=6)
    zoom = blocks.IntegerBlock(default=15)
    link = blocks.URLBlock()

    class Meta:
        icon = "globe"


class TextSection(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    is_main_title = blocks.BooleanBlock(required=False, default=False)
    subtitle = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)
    illustration = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("cathedral", "Cathedral"),
            ("florence", "Florence"),
            ("florence2", "Florence2"),
            ("handWithSnakeInside", "Hand With Snake Inside"),
            ("snake1", "Snake1"),
            ("snake2", "Snake2"),
            ("snake4", "Snake4"),
            ("snake5", "Snake5"),
            ("snakeBody", "Snake Body"),
            ("snakeCouple", "Snake Couple"),
            ("snakeDNA", "Snake D N A"),
            ("snakeHead", "Snake Head"),
            ("snakeInDragon", "Snake In Dragon"),
            ("snakeInDragonInverted", "Snake In Dragon Inverted"),
            ("snakeLetter", "Snake Letter"),
            ("snakeLongNeck", "Snake Long Neck"),
            ("snakePencil", "Snake Pencil"),
            ("snakeTail", "Snake Tail"),
            ("snakeWithBalloon", "Snake With Balloon"),
            ("snakeWithContacts", "Snake With Contacts"),
            ("snakesWithBanner", "Snakes With Banner"),
            ("snakesWithCocktail", "Snakes With Cocktail"),
            ("snakesWithDirections", "Snakes With Directions"),
            ("snakesWithOutlines", "Snakes With Outlines"),
            ("tripleSnakes", "Triple Snakes"),
        ],
        icon="image",
    )
    accordions = blocks.ListBlock(Accordion)
    cta = CTA()

    class Meta:
        icon = "doc-full"


class BodyBlock(blocks.StreamBlock):
    text_section = TextSection()
    map = Map()
    image = ImageChooserBlock()
    slider_cards_section = SliderCardsSection()
