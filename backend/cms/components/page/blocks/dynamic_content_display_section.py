from wagtail import blocks


class DynamicContentDisplaySection(blocks.StructBlock):
    source = blocks.ChoiceBlock(
        choices=[
            ("speakers", "Speakers"),
            ("keynoters", "Keynoters"),
            ("proposals", "Proposals"),
            ("communities", "Communities"),
        ],
    )
