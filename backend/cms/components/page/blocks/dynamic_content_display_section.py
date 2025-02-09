from wagtail import blocks


class DynamicContentDisplaySection(blocks.StructBlock):
    source = blocks.ChoiceBlock(
        choices=[
            ("speakers", "Speakers"),
            ("keynoters", "Keynoters"),
            ("accepted_proposals", "Accepted Proposals"),
        ],
    )
