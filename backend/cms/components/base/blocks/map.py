from wagtail import blocks


class Map(blocks.StructBlock):
    longitude = blocks.DecimalBlock(max_digits=11, decimal_places=8)
    latitude = blocks.DecimalBlock(max_digits=11, decimal_places=8)
    zoom = blocks.IntegerBlock(default=15)
    link = blocks.URLBlock()

    class Meta:
        icon = "globe"
