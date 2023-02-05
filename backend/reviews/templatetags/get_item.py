from typing import Any, Optional

from django import template

register = template.Library()


@register.filter
def get_item(dict: Optional[dict[str, Any]], key: str):
    if not dict:
        return ""

    return dict.get(str(key), "")
