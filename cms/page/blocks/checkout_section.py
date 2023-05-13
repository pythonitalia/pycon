from wagtail import blocks


class CheckoutSection(blocks.StructBlock):
    show_conference_tickets_products = blocks.BooleanBlock(
        required=False, default=False
    )
    show_social_events_products = blocks.BooleanBlock(required=False, default=False)
    show_tours_products = blocks.BooleanBlock(required=False, default=False)
    show_gadgets_products = blocks.BooleanBlock(required=False, default=False)
    show_membership_products = blocks.BooleanBlock(required=False, default=False)
    show_hotel_products = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        label = "Checkout Section"
        icon = "crosshairs"
