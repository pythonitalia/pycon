from wagtail import blocks


class HomepageHero(blocks.StructBlock):
    city = blocks.ChoiceBlock(
        choices=[
            ("florence", "Florence"),
            ("bologna", "Bologna"),
        ]
    )

    class Meta:
        label = "Homepage Hero"
        icon = "crosshairs"
