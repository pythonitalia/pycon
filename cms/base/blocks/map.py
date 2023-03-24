from wagtail import blocks


class Map(blocks.StructBlock):
    longitude = blocks.DecimalBlock(max_digits=9, decimal_places=6)
    latitude = blocks.DecimalBlock(max_digits=9, decimal_places=6)
    zoom = blocks.IntegerBlock(default=15)
    link = blocks.URLBlock()

    class Meta:
        icon = "globe"
