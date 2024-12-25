import json
from django import template
from django.utils.html import escapejs
from django.core.serializers.json import DjangoJSONEncoder

register = template.Library()

_json_script_escapes = {
    ord(">"): "\\u003E",
    ord("<"): "\\u003C",
    ord("&"): "\\u0026",
}


@register.filter
def to_json_for_prop(value):
    return escapejs(
        json.dumps(value, cls=DjangoJSONEncoder).translate(_json_script_escapes)
    )
