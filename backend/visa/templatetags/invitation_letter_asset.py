from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def invitation_letter_asset(context, asset_handle: str, **kwargs):
    config = context["config"]
    assets = config.assets.all()
    matching_asset = next(
        (asset for asset in assets if asset.handle == asset_handle), None
    )

    width = kwargs.get("width", None)
    height = kwargs.get("height", None)

    style_props = {}
    if width:
        style_props["width"] = width
    if height:
        style_props["height"] = height

    style_props_as_str = " ".join([f"{k}: {v}" for k, v in style_props.items()])
    return mark_safe(
        f'<img src="{matching_asset.image.url}" style="{style_props_as_str}" />'
    )
