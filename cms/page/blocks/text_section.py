from base.blocks.accordion import Accordion
from base.blocks.cta import CTA
from wagtail import blocks


class TextSection(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    is_main_title = blocks.BooleanBlock(required=False, default=False)
    subtitle = blocks.CharBlock(required=False)
    body = blocks.RichTextBlock(required=False)
    body_text_size = blocks.ChoiceBlock(
        required=False,
        default="text-1",
        choices=[("text-1", "Text-1"), ("text-2", "Text-2")],
    )
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
